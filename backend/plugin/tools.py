#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import json
import os
import subprocess
import sys
import warnings

from functools import lru_cache
from importlib.metadata import PackageNotFoundError, distribution
from typing import Any

import rtoml

from fastapi import APIRouter, Depends, Request
from packaging.requirements import Requirement
from starlette.concurrency import run_in_threadpool

from backend.common.enums import DataBaseType, PrimaryKeyType, StatusType
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import RedisCli, redis_client
from backend.utils._await import run_await
from backend.utils.import_parse import import_module_cached


class PluginConfigError(Exception):
    """Plugin configuration error"""


class PluginInjectError(Exception):
    """Plugin injection error"""


class PluginInstallError(Exception):
    """Plugin installation error"""


@lru_cache
def get_plugins() -> list[str]:
    """Get plugin list"""
    plugin_packages = []

    # Traverse plugin directory
    for item in os.listdir(PLUGIN_DIR):
        if not os.path.isdir(os.path.join(PLUGIN_DIR, item)) and item == '__pycache__':
            continue

        item_path = os.path.join(PLUGIN_DIR, item)

        # Check if it is a directory and contains __init__.py file
        if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
            plugin_packages.append(item)

    return plugin_packages


def get_plugin_models() -> list[type]:
    """Get all plugin model classes"""
    classes = []

    for plugin in get_plugins():
        # Import plugin's model module
        module_path = f'backend.plugin.{plugin}.model'
        module = import_module_cached(module_path)

        # Get all classes in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(obj)

    return classes


async def get_plugin_sql(plugin: str, db_type: DataBaseType, pk_type: PrimaryKeyType) -> str | None:
    """
    Get plugin SQL script

    :param plugin: Plugin name
    :param db_type: Database type
    :param pk_type: Primary key type
    :return:
    """
    if db_type == DataBaseType.mysql.value:
        mysql_dir = os.path.join(PLUGIN_DIR, plugin, 'sql', 'mysql')
        if pk_type == PrimaryKeyType.autoincrement:
            sql_file = os.path.join(mysql_dir, 'init.sql')
        else:
            sql_file = os.path.join(mysql_dir, 'init_snowflake.sql')
    else:
        postgresql_dir = os.path.join(PLUGIN_DIR, plugin, 'sql', 'postgresql')
        if pk_type == PrimaryKeyType.autoincrement.value:
            sql_file = os.path.join(postgresql_dir, 'init.sql')
        else:
            sql_file = os.path.join(postgresql_dir, 'init_snowflake.sql')

    if not os.path.exists(sql_file):
        return None

    return sql_file


def load_plugin_config(plugin: str) -> dict[str, Any]:
    """
    Load plugin configuration

    :param plugin: Plugin name
    :return:
    """
    toml_path = os.path.join(PLUGIN_DIR, plugin, 'plugin.toml')
    if not os.path.exists(toml_path):
        raise PluginInjectError(f'Plugin {plugin} is missing plugin.toml configuration file, please check if the plugin is valid')

    with open(toml_path, 'r', encoding='utf-8') as f:
        return rtoml.load(f)


def parse_plugin_config() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Parse plugin configuration"""

    extend_plugins = []
    app_plugins = []

    plugins = get_plugins()

    # Use independent singleton to avoid conflict with main thread
    current_redis_client = RedisCli()
    run_await(current_redis_client.open)()

    run_await(current_redis_client.delete_prefix)(f'{settings.PLUGIN_REDIS_PREFIX}:info', exclude=plugins)
    plugin_status = run_await(current_redis_client.hgetall)(f'{settings.PLUGIN_REDIS_PREFIX}:status')
    if not plugin_status:
        plugin_status = {}

    for plugin in plugins:
        data = load_plugin_config(plugin)

        plugin_info = data.get('plugin')
        if not plugin_info:
            raise PluginConfigError(f'Plugin {plugin} configuration file is missing plugin config')

        required_fields = ['summary', 'version', 'description', 'author']
        missing_fields = [field for field in required_fields if field not in plugin_info]
        if missing_fields:
            raise PluginConfigError(f'Plugin {plugin} configuration file is missing required fields: {", ".join(missing_fields)}')

        if data.get('api'):
            # TODO: Remove deprecated include config
            include = data.get('app', {}).get('include')
            if include:
                warnings.warn(
                    f'Plugin {plugin} config app.include will be deprecated in future versions, please update config to app.extend, details: https://fastapi-practices.github.io/fastapi_best_architecture_docs/plugin/dev.html#%E6%8F%92%E4%BB%B6%E9%85%8D%E7%BD%AE',
                    FutureWarning,
                )
            if not include and not data.get('app', {}).get('extend'):
                raise PluginConfigError(f'Extension-level plugin {plugin} configuration file is missing app.extend config')
            extend_plugins.append(data)
        else:
            if not data.get('app', {}).get('router'):
                raise PluginConfigError(f'Application-level plugin {plugin} configuration file is missing app.router config')
            app_plugins.append(data)

        # Supplement plugin info
        data['plugin']['enable'] = plugin_status.setdefault(plugin, str(StatusType.enable.value))
        data['plugin']['name'] = plugin

        # Cache plugin info
        run_await(current_redis_client.set)(
            f'{settings.PLUGIN_REDIS_PREFIX}:info:{plugin}', json.dumps(data, ensure_ascii=False)
        )

    # Cache plugin status
    run_await(current_redis_client.hset)(f'{settings.PLUGIN_REDIS_PREFIX}:status', mapping=plugin_status)
    run_await(current_redis_client.delete)(f'{settings.PLUGIN_REDIS_PREFIX}:changed')

    return extend_plugins, app_plugins


def inject_extend_router(plugin: dict[str, Any]) -> None:
    """
    Extension-level plugin router injection

    :param plugin: Plugin name
    :return:
    """
    plugin_name: str = plugin['plugin']['name']
    plugin_api_path = os.path.join(PLUGIN_DIR, plugin_name, 'api')
    if not os.path.exists(plugin_api_path):
        raise PluginConfigError(f'Plugin {plugin} is missing api directory, please check if plugin files are complete')

    for root, _, api_files in os.walk(plugin_api_path):
        for file in api_files:
            if not (file.endswith('.py') and file != '__init__.py'):
                continue

            # Parse plugin router config
            file_config = plugin['api'][file[:-3]]
            prefix = file_config['prefix']
            tags = file_config['tags']

            # Get plugin router module
            file_path = os.path.join(root, file)
            path_to_module_str = os.path.relpath(file_path, PLUGIN_DIR).replace(os.sep, '.')[:-3]
            module_path = f'backend.plugin.{path_to_module_str}'

            try:
                module = import_module_cached(module_path)
                plugin_router = getattr(module, 'router', None)
                if not plugin_router:
                    warnings.warn(
                        f'Extension-level plugin {plugin_name} module {module_path} does not have a valid router, please check if plugin files are complete',
                        FutureWarning,
                    )
                    continue

                # Get target app router
                relative_path = os.path.relpath(root, plugin_api_path)
                # TODO: Remove deprecated include config
                app_name = plugin.get('app', {}).get('include') or plugin.get('app', {}).get('extend')
                target_module_path = f'backend.app.{app_name}.api.{relative_path.replace(os.sep, ".")}'
                target_module = import_module_cached(target_module_path)
                target_router = getattr(target_module, 'router', None)

                if not target_router or not isinstance(target_router, APIRouter):
                    raise PluginInjectError(
                        f'Extension-level plugin {plugin_name} module {module_path} does not have a valid router, please check if plugin files are complete'
                    )

                # Inject plugin router into target router
                target_router.include_router(
                    router=plugin_router,
                    prefix=prefix,
                    tags=[tags] if tags else [],
                    dependencies=[Depends(PluginStatusChecker(plugin_name))],
                )
            except Exception as e:
                raise PluginInjectError(f'Extension-level plugin {plugin_name} router injection failed: {str(e)}') from e


def inject_app_router(plugin: dict[str, Any], target_router: APIRouter) -> None:
    """
    Application-level plugin router injection

    :param plugin: Plugin name
    :param target_router: FastAPI router
    :return:
    """
    plugin_name: str = plugin['plugin']['name']
    module_path = f'backend.plugin.{plugin_name}.api.router'
    try:
        module = import_module_cached(module_path)
        routers = plugin['app']['router']
        if not routers or not isinstance(routers, list):
            raise PluginConfigError(f'Application-level plugin {plugin_name} configuration file has errors, please check')

        for router in routers:
            plugin_router = getattr(module, router, None)
            if not plugin_router or not isinstance(plugin_router, APIRouter):
                raise PluginInjectError(
                    f'Application-level plugin {plugin_name} module {module_path} does not have a valid router, please check if plugin files are complete'
                )

            # Inject plugin router into target router
            target_router.include_router(plugin_router, dependencies=[Depends(PluginStatusChecker(plugin_name))])
    except Exception as e:
        raise PluginInjectError(f'Application-level plugin {plugin_name} router injection failed: {str(e)}') from e


def build_final_router() -> APIRouter:
    """Build final router"""
    extend_plugins, app_plugins = parse_plugin_config()

    for plugin in extend_plugins:
        inject_extend_router(plugin)

    # Main router, must be imported after extension-level plugin router injection and before application-level plugin router injection
    from backend.app.router import router as main_router

    for plugin in app_plugins:
        inject_app_router(plugin, main_router)

    return main_router


def install_requirements(plugin: str | None) -> None:
    """
    Install plugin dependencies

    :param plugin: Specify plugin name, otherwise check all plugins
    :return:
    """
    plugins = [plugin] if plugin else get_plugins()

    for plugin in plugins:
        requirements_file = os.path.join(PLUGIN_DIR, plugin, 'requirements.txt')
        missing_dependencies = False
        if os.path.exists(requirements_file):
            with open(requirements_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    try:
                        req = Requirement(line)
                        dependency = req.name.lower()
                    except Exception as e:
                        raise PluginInstallError(f'Plugin {plugin} dependency {line} format error: {str(e)}') from e
                    try:
                        distribution(dependency)
                    except PackageNotFoundError:
                        missing_dependencies = True

        if missing_dependencies:
            try:
                ensurepip_install = [sys.executable, '-m', 'ensurepip', '--upgrade']
                pip_install = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
                if settings.PLUGIN_PIP_CHINA:
                    pip_install.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])
                subprocess.check_call(ensurepip_install, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.check_call(pip_install, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                raise PluginInstallError(f'Plugin {plugin} dependency installation failed: {e}') from e


def uninstall_requirements(plugin: str) -> None:
    """
    Uninstall plugin dependencies

    :param plugin: Plugin name
    :return:
    """
    requirements_file = os.path.join(PLUGIN_DIR, plugin, 'requirements.txt')
    if os.path.exists(requirements_file):
        try:
            pip_uninstall = [sys.executable, '-m', 'pip', 'uninstall', '-r', requirements_file, '-y']
            subprocess.check_call(pip_uninstall, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            raise PluginInstallError(f'Plugin {plugin} dependency uninstallation failed: {e}') from e


async def install_requirements_async(plugin: str | None = None) -> None:
    """
    Asynchronously install plugin dependencies

    Due to Windows platform limitations, a perfect fully asynchronous solution cannot be achieved. Details:
    https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
    """
    await run_in_threadpool(install_requirements, plugin)


async def uninstall_requirements_async(plugin: str) -> None:
    """
    Asynchronously uninstall plugin dependencies

    :param plugin: Plugin name
    :return:
    """
    await run_in_threadpool(uninstall_requirements, plugin)


class PluginStatusChecker:
    """Plugin status checker"""

    def __init__(self, plugin: str) -> None:
        """
        Initialize plugin status checker

        :param plugin: Plugin name
        :return:
        """
        self.plugin = plugin

    async def __call__(self, request: Request) -> None:
        """
        Validate plugin status

        :param request: FastAPI request object
        :return:
        """
        plugin_status = await redis_client.hgetall(f'{settings.PLUGIN_REDIS_PREFIX}:status')
        if not plugin_status:
            log.error('Plugin status not initialized or lost, need to restart service to auto repair')
            raise PluginInjectError('Plugin status not initialized or lost, please contact system administrator')

        if self.plugin not in plugin_status:
            log.error(f'Plugin {self.plugin} status not initialized or lost, need to restart service to auto repair')
            raise PluginInjectError(f'Plugin {self.plugin} status not initialized or lost, please contact system administrator')
        if not int(plugin_status.get(self.plugin)):
            raise errors.ServerError(msg=f'Plugin {self.plugin} is not enabled, please contact system administrator')

