#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.task.model.result import TaskResult


class CRUDTaskResult(CRUDPlus[TaskResult]):
    """Database operations class for task results"""

    async def get(self, db: AsyncSession, pk: int) -> TaskResult | None:
        """
        Get task result details

        :param db: Database session
        :param pk: Task ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, name: str | None, task_id: str | None) -> Select:
        """
        Get list of task results

        :param name: Task name
        :param task_id: Task ID
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if task_id is not None:
            filters['task_id'] = task_id

        return await self.select_order('id', **filters)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Batch delete task results

        :param db: Database session
        :param pks: List of task result IDs
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


task_result_dao: CRUDTaskResult = CRUDTaskResult(TaskResult)
