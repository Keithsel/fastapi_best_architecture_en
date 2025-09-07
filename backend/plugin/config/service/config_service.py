#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.config.crud.crud_config import config_dao
from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import (
    CreateConfigParam,
    UpdateConfigParam,
    UpdateConfigsParam,
)


class ConfigService:
    """Configuration parameter service class"""

    @staticmethod
    async def get(*, pk: int) -> Config:
        """
        Get configuration parameter details

        :param pk: Configuration parameter ID
        :return:
        """
        async with async_db_session() as db:
            config = await config_dao.get(db, pk)
            if not config:
                raise errors.NotFoundError(msg='Configuration parameter does not exist')
            return config

    @staticmethod
    async def get_all(*, type: str | None):
        """
        Get all configuration parameters

        :param type: Configuration parameter type
        :return:
        """
        async with async_db_session() as db:
            return await config_dao.get_all(db, type)

    @staticmethod
    async def get_select(*, name: str | None, type: str | None) -> Select:
        """
        Get query conditions for configuration parameter list

        :param name: Configuration parameter name
        :param type: Configuration parameter type
        :return:
        """
        return await config_dao.get_list(name=name, type=type)

    @staticmethod
    async def create(*, obj: CreateConfigParam) -> None:
        """
        Create configuration parameter

        :param obj: Configuration parameter creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            config = await config_dao.get_by_key(db, obj.key)
            if config:
                raise errors.ConflictError(msg=f'Configuration parameter {obj.key} already exists')
            await config_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateConfigParam) -> int:
        """
        Update configuration parameter

        :param pk: Configuration parameter ID
        :param obj: Configuration parameter update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            config = await config_dao.get(db, pk)
            if not config:
                raise errors.NotFoundError(msg='Configuration parameter does not exist')
            if config.key != obj.key:
                config = await config_dao.get_by_key(db, obj.key)
                if config:
                    raise errors.ConflictError(msg=f'Configuration parameter {obj.key} already exists')
            count = await config_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def bulk_update(*, objs: list[UpdateConfigsParam]) -> int:
        """
        Bulk update configuration parameters

        :param objs: Bulk update configuration parameter parameters
        :return:
        """
        async with async_db_session.begin() as db:
            for batch in range(0, len(objs), 1000):
                for obj in objs:
                    config = await config_dao.get(db, obj.id)
                    if not config:
                        raise errors.NotFoundError(msg='Configuration parameter does not exist')
                    if config.key != obj.key:
                        config = await config_dao.get_by_key(db, obj.key)
                        if config:
                            raise errors.ConflictError(msg=f'Configuration parameter {obj.key} already exists')
            count = await config_dao.bulk_update(db, objs)
            return count

    @staticmethod
    async def delete(*, pks: list[int]) -> int:
        """
        Batch delete configuration parameters

        :param pks: List of configuration parameter IDs
        :return:
        """
        async with async_db_session.begin() as db:
            count = await config_dao.delete(db, pks)
            return count


config_service: ConfigService = ConfigService()
