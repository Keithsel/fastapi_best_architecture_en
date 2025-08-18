#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.dict.model import DictType
from backend.plugin.dict.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam


class CRUDDictType(CRUDPlus[DictType]):
    """Dictionary Type Database Operation Class"""

    async def get(self, db: AsyncSession, pk: int) -> DictType | None:
        """
        Get dictionary type details

        :param db: Database session
        :param pk: Dictionary type ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, *, name: str | None, code: str | None, status: int | None) -> Select:
        """
        Get dictionary type list

        :param name: Dictionary type name
        :param code: Dictionary type code
        :param status: Dictionary status
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if code is not None:
            filters['code__like'] = f'%{code}%'
        if status is not None:
            filters['status'] = status

        return await self.select_order('id', 'desc', load_strategies={'datas': 'noload'}, **filters)

    async def get_by_code(self, db: AsyncSession, code: str) -> DictType | None:
        """
        Get dictionary type by code

        :param db: Database session
        :param code: Dictionary code
        :return:
        """
        return await self.select_model_by_column(db, code=code)

    async def create(self, db: AsyncSession, obj: CreateDictTypeParam) -> None:
        """
        Create dictionary type

        :param db: Database session
        :param obj: Create dictionary type parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDictTypeParam) -> int:
        """
        Update dictionary type

        :param db: Database session
        :param pk: Dictionary type ID
        :param obj: Update dictionary type parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Batch delete dictionary types

        :param db: Database session
        :param pks: List of dictionary type IDs
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


dict_type_dao: CRUDDictType = CRUDDictType(DictType)
