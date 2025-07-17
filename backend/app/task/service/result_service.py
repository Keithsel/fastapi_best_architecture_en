#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.task.crud.crud_result import task_result_dao
from backend.app.task.model.result import TaskResult
from backend.app.task.schema.result import DeleteTaskResultParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class TaskResultService:
    @staticmethod
    async def get(*, pk: int) -> TaskResult:
        """
        Get task result details

        :param pk: Task ID
        :return:
        """
        async with async_db_session() as db:
            result = await task_result_dao.get(db, pk)
            if not result:
                raise errors.NotFoundError(msg='Task result does not exist')
            return result

    @staticmethod
    async def get_select(*, name: str | None, task_id: str | None) -> Select:
        """
        Get query conditions for task result list

        :param name: Task name
        :param task_id: Task ID
        :return:
        """
        return await task_result_dao.get_list(name, task_id)

    @staticmethod
    async def delete(*, obj: DeleteTaskResultParam) -> int:
        """
        Batch delete task results

        :param obj: List of task result IDs
        :return:
        """
        async with async_db_session.begin() as db:
            count = await task_result_dao.delete(db, obj.pks)
            return count


task_result_service: TaskResultService = TaskResultService()
