#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.code_generator.crud.crud_column import gen_column_dao
from backend.plugin.code_generator.enums import GenMySQLColumnType
from backend.plugin.code_generator.model import GenColumn
from backend.plugin.code_generator.schema.column import CreateGenColumnParam, UpdateGenColumnParam
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_pydantic


class GenColumnService:
    """Code Generation Model Column Service Class"""

    @staticmethod
    async def get(*, pk: int) -> GenColumn:
        """
        Get model column by specified ID

        :param pk: Model column ID
        :return:
        """
        async with async_db_session() as db:
            column = await gen_column_dao.get(db, pk)
            if not column:
                raise errors.NotFoundError(msg='Code generation model column does not exist')
            return column

    @staticmethod
    async def get_types() -> list[str]:
        """Get all MySQL column types"""
        types = GenMySQLColumnType.get_member_keys()
        types.sort()
        return types

    @staticmethod
    async def get_columns(*, business_id: int) -> Sequence[GenColumn]:
        """
        Get all model columns for the specified business

        :param business_id: Business ID
        :return:
        """
        async with async_db_session() as db:
            return await gen_column_dao.get_all_by_business(db, business_id)

    @staticmethod
    async def create(*, obj: CreateGenColumnParam) -> None:
        """
        Create model column

        :param obj: Create model column parameters
        :return:
        """
        async with async_db_session.begin() as db:
            gen_columns = await gen_column_dao.get_all_by_business(db, obj.gen_business_id)
            if obj.name in [gen_column.name for gen_column in gen_columns]:
                raise errors.ForbiddenError(msg='Model column already exists')

            pd_type = sql_type_to_pydantic(obj.type)
            await gen_column_dao.create(db, obj, pd_type=pd_type)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenColumnParam) -> int:
        """
        Update model column

        :param pk: Model column ID
        :param obj: Update model column parameters
        :return:
        """
        async with async_db_session.begin() as db:
            column = await gen_column_dao.get(db, pk)
            if obj.name != column.name:
                gen_columns = await gen_column_dao.get_all_by_business(db, obj.gen_business_id)
                if obj.name in [gen_column.name for gen_column in gen_columns]:
                    raise errors.ConflictError(msg='Model column name already exists')

            pd_type = sql_type_to_pydantic(obj.type)
            return await gen_column_dao.update(db, pk, obj, pd_type=pd_type)

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        Delete model column

        :param pk: Model column ID
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_column_dao.delete(db, pk)


gen_column_service: GenColumnService = GenColumnService()
