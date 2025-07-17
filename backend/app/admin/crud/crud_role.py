#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataScope, Menu, Role
from backend.app.admin.schema.role import (
    CreateRoleParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleScopeParam,
)


class CRUDRole(CRUDPlus[Role]):
    """Role database operation class"""

    async def get(self, db: AsyncSession, role_id: int) -> Role | None:
        """
        Get role details

        :param db: Database session
        :param role_id: Role ID
        :return:
        """
        return await self.select_model(db, role_id)

    async def get_with_relation(self, db: AsyncSession, role_id: int) -> Role | None:
        """
        Get role and related data

        :param db: Database session
        :param role_id: Role ID
        :return:
        """
        return await self.select_model(db, role_id, load_strategies=['menus', 'scopes'])

    async def get_all(self, db: AsyncSession) -> Sequence[Role]:
        """
        Get all roles

        :param db: Database session
        :return:
        """
        return await self.select_models(db)

    async def get_list(self, name: str | None, status: int | None) -> Select:
        """
        Get role list

        :param name: Role name
        :param status: Role status
        :return:
        """

        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if status is not None:
            filters['status'] = status

        return await self.select_order(
            'id',
            load_strategies={
                'users': 'noload',
                'menus': 'noload',
                'scopes': 'noload',
            },
            **filters,
        )

    async def get_by_name(self, db: AsyncSession, name: str) -> Role | None:
        """
        Get role by name

        :param db: Database session
        :param name: Role name
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def create(self, db: AsyncSession, obj: CreateRoleParam) -> None:
        """
        Create role

        :param db: Database session
        :param obj: Create role parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, role_id: int, obj: UpdateRoleParam) -> int:
        """
        Update role

        :param db: Database session
        :param role_id: Role ID
        :param obj: Update role parameters
        :return:
        """
        return await self.update_model(db, role_id, obj)

    async def update_menus(self, db: AsyncSession, role_id: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        Update role menus

        :param db: Database session
        :param role_id: Role ID
        :param menu_ids: List of menu IDs
        :return:
        """
        current_role = await self.get_with_relation(db, role_id)
        stmt = select(Menu).where(Menu.id.in_(menu_ids.menus))
        menus = await db.execute(stmt)
        current_role.menus = menus.scalars().all()
        return len(current_role.menus)

    async def update_scopes(self, db: AsyncSession, role_id: int, scope_ids: UpdateRoleScopeParam) -> int:
        """
        Update role data scopes

        :param db: Database session
        :param role_id: Role ID
        :param scope_ids: List of scope IDs
        :return:
        """
        current_role = await self.get_with_relation(db, role_id)
        stmt = select(DataScope).where(DataScope.id.in_(scope_ids.scopes))
        scopes = await db.execute(stmt)
        current_role.scopes = scopes.scalars().all()
        return len(current_role.scopes)

    async def delete(self, db: AsyncSession, role_ids: list[int]) -> int:
        """
        Batch delete roles

        :param db: Database session
        :param role_ids: List of role IDs
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=role_ids)


role_dao: CRUDRole = CRUDRole(Role)
