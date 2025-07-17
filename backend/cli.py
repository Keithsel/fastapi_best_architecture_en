#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from dataclasses import dataclass
from typing import Annotated

import cappa
import granian

from rich.panel import Panel
from rich.text import Text
from sqlalchemy import text
from watchfiles import PythonFilter

from backend import console, get_version
from backend.common.enums import DataBaseType, PrimaryKeyType
from backend.common.exception.errors import BaseExceptionMixin
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.plugin.tools import get_plugin_sql
from backend.utils.file_ops import install_git_plugin, install_zip_plugin, parse_sql_script


def run(host: str, port: int, reload: bool, workers: int | None) -> None:
    url = f'http://{host}:{port}'
    docs_url = url + settings.FASTAPI_DOCS_URL
    redoc_url = url + settings.FASTAPI_REDOC_URL
    openapi_url = url + settings.FASTAPI_OPENAPI_URL

    panel_content = Text()
    panel_content.append(f'📝 Swagger Docs: {docs_url}\n', style='blue')
    panel_content.append(f'📚 Redoc   Docs: {redoc_url}\n', style='yellow')
    panel_content.append(f'📡 OpenAPI JSON: {openapi_url}\n', style='green')
    panel_content.append(
        '🌍 fba Official Docs: https://fastapi-practices.github.io/fastapi_best_architecture_docs/',
        style='cyan',
    )

    console.print(Panel(panel_content, title='fba Service Info', border_style='purple', padding=(1, 2)))
    granian.Granian(
        target='backend.main:app',
        interface='asgi',
        address=host,
        port=port,
        reload=not reload,
        reload_filter=PythonFilter(),
        workers=workers or 1,
    ).serve()


async def install_plugin(
    path: str, repo_url: str, no_sql: bool, db_type: DataBaseType, pk_type: PrimaryKeyType
) -> None:
    if not path and not repo_url:
        raise cappa.Exit('Either path or repo_url must be specified', code=1)
    if path and repo_url:
        raise cappa.Exit('path and repo_url cannot be specified at the same time', code=1)

    plugin_name = None
    console.print(Text('Starting plugin installation...', style='bold cyan'))

    try:
        if path:
            plugin_name = await install_zip_plugin(file=path)
        if repo_url:
            plugin_name = await install_git_plugin(repo_url=repo_url)

        console.print(Text(f'Plugin {plugin_name} installed successfully', style='bold green'))

        sql_file = await get_plugin_sql(plugin_name, db_type, pk_type)
        if sql_file and not no_sql:
            console.print(Text('Automatically executing plugin SQL script...', style='bold cyan'))
            await execute_sql_scripts(sql_file)

    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionMixin) else str(e), code=1)


async def execute_sql_scripts(sql_scripts: str) -> None:
    async with async_db_session.begin() as db:
        try:
            stmts = await parse_sql_script(sql_scripts)
            for stmt in stmts:
                await db.execute(text(stmt))
        except Exception as e:
            raise cappa.Exit(f'SQL script execution failed: {e}', code=1)

    console.print(Text('SQL script executed successfully', style='bold green'))


@cappa.command(help='Run the service')
@dataclass
class Run:
    host: Annotated[
        str,
        cappa.Arg(
            long=True,
            default='127.0.0.1',
            help='Host IP address to provide the service. For local development, use `127.0.0.1`.'
            'To enable public access, such as on a LAN, use `0.0.0.0`',
        ),
    ]
    port: Annotated[
        int,
        cappa.Arg(long=True, default=8000, help='Port number to provide the service'),
    ]
    no_reload: Annotated[
        bool,
        cappa.Arg(long=True, default=False, help='Disable automatic server reload on (code) file changes'),
    ]
    workers: Annotated[
        int | None,
        cappa.Arg(long=True, default=None, help='Use multiple worker processes, must be used with `--no-reload`'),
    ]

    def __call__(self):
        run(host=self.host, port=self.port, reload=self.no_reload, workers=self.workers)


@cappa.command(help='Add a plugin')
@dataclass
class Add:
    path: Annotated[
        str | None,
        cappa.Arg(long=True, help='Full local path to the ZIP plugin'),
    ]
    repo_url: Annotated[
        str | None,
        cappa.Arg(long=True, help='Git repository URL of the plugin'),
    ]
    no_sql: Annotated[
        bool,
        cappa.Arg(long=True, default=False, help='Disable automatic execution of plugin SQL scripts'),
    ]
    db_type: Annotated[
        DataBaseType,
        cappa.Arg(long=True, default='mysql', help='Database type for executing plugin SQL scripts'),
    ]
    pk_type: Annotated[
        PrimaryKeyType,
        cappa.Arg(long=True, default='autoincrement', help='Primary key type for plugin SQL script database'),
    ]

    async def __call__(self):
        await install_plugin(self.path, self.repo_url, self.no_sql, self.db_type, self.pk_type)


@cappa.command(help='An efficient fba command line interface')
@dataclass
class FbaCli:
    version: Annotated[
        bool,
        cappa.Arg(short='-V', long=True, default=False, help='Print current version'),
    ]
    sql: Annotated[
        str,
        cappa.Arg(long=True, default='', help='Execute SQL script in a transaction'),
    ]
    subcmd: cappa.Subcommands[Run | Add | None] = None

    async def __call__(self):
        if self.version:
            get_version()
        if self.sql:
            await execute_sql_scripts(self.sql)


def main() -> None:
    output = cappa.Output(error_format='[red]Error[/]: {message}\n\nFor more info, try "[cyan]--help[/]"')
    asyncio.run(cappa.invoke_async(FbaCli, output=output))
