#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.admin.crud.crud_opera_log import opera_log_dao
from backend.app.admin.schema.opera_log import CreateOperaLogParam, DeleteOperaLogParam
from backend.database.db import async_db_session


class OperaLogService:
    """Operation Log Service Class"""

    @staticmethod
    async def get_select(*, username: str | None, status: int | None, ip: str | None) -> Select:
        """
        Get operation log list query conditions

        :param username: Username
        :param status: Status
        :param ip: IP address
        :return:
        """
        return await opera_log_dao.get_list(username=username, status=status, ip=ip)

    @staticmethod
    async def create(*, obj: CreateOperaLogParam) -> None:
        """
        Create operation log

        :param obj: Operation log creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            await opera_log_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateOperaLogParam]) -> None:
        """
        批量创建操作日志

        :param objs: 操作日志创建参数列表
        :return:
        """
        async with async_db_session.begin() as db:
            await opera_log_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteOperaLogParam) -> int:
        """
        Batch delete operation logs

        :param obj: List of log IDs
        :return:
        """
        async with async_db_session.begin() as db:
            count = await opera_log_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        """Clear all operation logs"""
        async with async_db_session.begin() as db:
            await opera_log_dao.delete_all(db)


opera_log_service: OperaLogService = OperaLogService()
