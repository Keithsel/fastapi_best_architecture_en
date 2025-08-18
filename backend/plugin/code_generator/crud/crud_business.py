#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam, UpdateGenBusinessParam


class CRUDGenBusiness(CRUDPlus[GenBusiness]):
    """Code Generation Business CRUD Class"""

    async def get(self, db: AsyncSession, pk: int) -> GenBusiness | None:
        """
        Get code generation business

        :param db: Database session
        :param pk: Code generation business ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> GenBusiness | None:
        """
        Get code generation business by name

        :param db: Database session
        :param name: Table name
        :return:
        """
        return await self.select_model_by_column(db, table_name=name)

    async def get_all(self, db: AsyncSession) -> Sequence[GenBusiness]:
        """
        Get all code generation businesses

        :param db: Database session
        :return:
        """
        return await self.select_models(db)

    async def get_list(self, table_name: str | None) -> Select:
        """
        Get all code generation businesses

        :param table_name: Business table name
        :return:
        """
        filters = {}

        if table_name is not None:
            filters['table_name__like'] = f'%{table_name}%'

        return await self.select_order('id', 'desc', load_strategies={'gen_column': 'noload'}, **filters)

    async def create(self, db: AsyncSession, obj: CreateGenBusinessParam) -> None:
        """
        Create code generation business

        :param db: Database session
        :param obj: Create code generation business parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateGenBusinessParam) -> int:
        """
        Update code generation business

        :param db: Database session
        :param pk: Code generation business ID
        :param obj: Update code generation business parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        Delete code generation business

        :param db: Database session
        :param pk: Code generation business ID
        :return:
        """
        return await self.delete_model(db, pk)


gen_business_dao: CRUDGenBusiness = CRUDGenBusiness(GenBusiness)
