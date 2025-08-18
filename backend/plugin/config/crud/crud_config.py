#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import CreateConfigParam, UpdateConfigParam


class CRUDConfig(CRUDPlus[Config]):
    """System parameter configuration database operation class"""

    async def get(self, db: AsyncSession, pk: int) -> Config | None:
        """
        Get parameter configuration details

        :param db: Database session
        :param pk: Parameter configuration ID
        :return:
        """
        return await self.select_model_by_column(db, id=pk)

    async def get_by_type(self, db: AsyncSession, type: str) -> Sequence[Config | None]:
        """
        Get parameter configuration by type

        :param db: Database session
        :param type: Parameter configuration type
        :return:
        """
        return await self.select_models(db, type=type)

    async def get_by_key(self, db: AsyncSession, key: str) -> Config | None:
        """
        Get parameter configuration by key

        :param db: Database session
        :param key: Parameter configuration key
        :return:
        """
        return await self.select_model_by_column(db, key=key)

    async def get_list(self, name: str | None, type: str | None) -> Select:
        """
        Get parameter configuration list

        :param name: Parameter configuration name
        :param type: Parameter configuration type
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if type is not None:
            filters['type__like'] = f'%{type}%'

        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateConfigParam) -> None:
        """
        Create parameter configuration

        :param db: Database session
        :param obj: Create parameter configuration parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateConfigParam) -> int:
        """
        Update parameter configuration

        :param db: Database session
        :param pk: Parameter configuration ID
        :param obj: Update parameter configuration parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Batch delete parameter configurations

        :param db: Database session
        :param pks: Parameter configuration ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


config_dao: CRUDConfig = CRUDConfig(Config)
