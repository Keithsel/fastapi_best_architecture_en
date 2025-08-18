#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.code_generator.crud.crud_business import gen_business_dao
from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam, UpdateGenBusinessParam


class GenBusinessService:
    """Code Generation Business Service Class"""

    @staticmethod
    async def get(*, pk: int) -> GenBusiness:
        """
        Get business by specified ID

        :param pk: Business ID
        :return:
        """
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='Code generation business does not exist')
            return business

    @staticmethod
    async def get_all() -> Sequence[GenBusiness]:
        """Get all businesses"""
        async with async_db_session() as db:
            return await gen_business_dao.get_all(db)

    @staticmethod
    async def get_select(*, table_name: str) -> Select:
        """
        Get query condition for code generation business list

        :param table_name: Business table name
        :return:
        """
        return await gen_business_dao.get_list(table_name=table_name)

    @staticmethod
    async def create(*, obj: CreateGenBusinessParam) -> None:
        """
        Create business

        :param obj: Parameters for creating business
        :return:
        """
        async with async_db_session.begin() as db:
            business = await gen_business_dao.get_by_name(db, obj.table_name)
            if business:
                raise errors.ConflictError(msg='Code generation business already exists')
            await gen_business_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenBusinessParam) -> int:
        """
        Update business

        :param pk: Business ID
        :param obj: Parameters for updating business
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_business_dao.update(db, pk, obj)

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        Delete business

        :param pk: Business ID
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_business_dao.delete(db, pk)


gen_business_service: GenBusinessService = GenBusinessService()
