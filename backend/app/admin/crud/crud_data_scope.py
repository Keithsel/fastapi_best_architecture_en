#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRule, DataScope
from backend.app.admin.schema.data_scope import CreateDataScopeParam, UpdateDataScopeParam, UpdateDataScopeRuleParam


class CRUDDataScope(CRUDPlus[DataScope]):
    """Data scope database operation class"""

    async def get(self, db: AsyncSession, pk: int) -> DataScope | None:
        """
        Get data scope details

        :param db: Database session
        :param pk: Scope ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> DataScope | None:
        """
        Get data scope by name

        :param db: Database session
        :param name: Scope name
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def get_with_relation(self, db: AsyncSession, pk: int) -> DataScope:
        """
        Get data scope with related data

        :param db: Database session
        :param pk: Scope ID
        :return:
        """
        return await self.select_model(db, pk, load_strategies=['rules'])

    async def get_all(self, db: AsyncSession) -> Sequence[DataScope]:
        """
        Get all data scopes

        :param db: Database session
        :return:
        """
        return await self.select_models(db)

    async def get_list(self, name: str | None, status: int | None) -> Select:
        """
        Get data scope list

        :param name: Scope name
        :param status: Scope status
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if status is not None:
            filters['status'] = status

        return await self.select_order('id', load_strategies={'rules': 'noload', 'roles': 'noload'}, **filters)

    async def create(self, db: AsyncSession, obj: CreateDataScopeParam) -> None:
        """
        Create data scope

        :param db: Database session
        :param obj: Create data scope parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDataScopeParam) -> int:
        """
        Update data scope

        :param db: Database session
        :param pk: Scope ID
        :param obj: Update data scope parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def update_rules(self, db: AsyncSession, pk: int, rule_ids: UpdateDataScopeRuleParam) -> int:
        """
        Update data scope rules

        :param db: Database session
        :param pk: Scope ID
        :param rule_ids: Data rule ID list
        :return:
        """
        current_data_scope = await self.get_with_relation(db, pk)
        stmt = select(DataRule).where(DataRule.id.in_(rule_ids.rules))
        rules = await db.execute(stmt)
        current_data_scope.rules = rules.scalars().all()
        return len(current_data_scope.rules)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Batch delete data scopes

        :param db: Database session
        :param pks: Scope ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


data_scope_dao: CRUDDataScope = CRUDDataScope(DataScope)
