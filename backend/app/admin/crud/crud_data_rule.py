#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import CreateDataRuleParam, UpdateDataRuleParam


class CRUDDataRule(CRUDPlus[DataRule]):
    """Data rule database operation class"""

    async def get(self, db: AsyncSession, pk: int) -> DataRule | None:
        """
        Get rule details

        :param db: Database session
        :param pk: Rule ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, name: str | None) -> Select:
        """
        Get rule list

        :param name: Rule name
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'

        return await self.select_order('id', load_strategies={'scopes': 'noload'}, **filters)

    async def get_by_name(self, db: AsyncSession, name: str) -> DataRule | None:
        """
        Get rule by name

        :param db: Database session
        :param name: Rule name
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def get_all(self, db: AsyncSession) -> Sequence[DataRule]:
        """
        Get all rules

        :param db: Database session
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj: CreateDataRuleParam) -> None:
        """
        Create rule

        :param db: Database session
        :param obj: Create rule parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDataRuleParam) -> int:
        """
        Update rule

        :param db: Database session
        :param pk: Rule ID
        :param obj: Update rule parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Batch delete rules

        :param db: Database session
        :param pks: Rule ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


data_rule_dao: CRUDDataRule = CRUDDataRule(DataRule)

