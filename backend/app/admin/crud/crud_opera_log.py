#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import OperaLog
from backend.app.admin.schema.opera_log import CreateOperaLogParam


class CRUDOperaLogDao(CRUDPlus[OperaLog]):
    """Operation log database operation class"""

    async def get_list(self, username: str | None, status: int | None, ip: str | None) -> Select:
        """
        Get operation log list

        :param username: Username
        :param status: Operation status
        :param ip: IP address
        :return:
        """
        filters = {}

        if username is not None:
            filters['username__like'] = f'%{username}%'
        if status is not None:
            filters['status__eq'] = status
        if ip is not None:
            filters['ip__like'] = f'%{ip}%'

        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateOperaLogParam) -> None:
        """
        Create operation log

        :param db: Database session
        :param obj: Create operation log parameters
        :return:
        """
        await self.create_model(db, obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Batch delete operation logs

        :param db: Database session
        :param pks: Operation log ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    async def delete_all(self, db: AsyncSession) -> int:
        """
        Delete all logs

        :param db: Database session
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True)


opera_log_dao: CRUDOperaLogDao = CRUDOperaLogDao(OperaLog)
