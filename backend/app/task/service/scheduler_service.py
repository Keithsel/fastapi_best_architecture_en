#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from typing import Sequence

from sqlalchemy import Select
from starlette.concurrency import run_in_threadpool

from backend.app.task.celery import celery_app
from backend.app.task.crud.crud_scheduler import task_scheduler_dao
from backend.app.task.enums import TaskSchedulerType
from backend.app.task.model import TaskScheduler
from backend.app.task.schema.scheduler import CreateTaskSchedulerParam, UpdateTaskSchedulerParam
from backend.app.task.utils.tzcrontab import crontab_verify
from backend.common.exception import errors
from backend.database.db import async_db_session


class TaskSchedulerService:
    """Task Scheduler Service Class"""

    @staticmethod
    async def get(*, pk) -> TaskScheduler | None:
        """
        Get task scheduler details

        :param pk: Task scheduler ID
        :return:
        """
        async with async_db_session() as db:
            task_scheduler = await task_scheduler_dao.get(db, pk)
            if not task_scheduler:
                raise errors.NotFoundError(msg='Task scheduler does not exist')
            return task_scheduler

    @staticmethod
    async def get_all() -> Sequence[TaskScheduler]:
        """Get all task schedulers"""
        async with async_db_session() as db:
            task_schedulers = await task_scheduler_dao.get_all(db)
            return task_schedulers

    @staticmethod
    async def get_select(*, name: str | None, type: int | None) -> Select:
        """
        Get query conditions for task scheduler list

        :param name: Task scheduler name
        :param type: Task scheduler type
        :return:
        """
        return await task_scheduler_dao.get_list(name=name, type=type)

    @staticmethod
    async def create(*, obj: CreateTaskSchedulerParam) -> None:
        """
        Create a task scheduler

        :param obj: Task scheduler creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            task_scheduler = await task_scheduler_dao.get_by_name(db, obj.name)
            if task_scheduler:
                raise errors.ConflictError(msg='Task scheduler already exists')
            await task_scheduler_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateTaskSchedulerParam) -> int:
        """
        Update a task scheduler

        :param pk: Task scheduler ID
        :param obj: Task scheduler update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            task_scheduler = await task_scheduler_dao.get(db, pk)
            if not task_scheduler:
                raise errors.NotFoundError(msg='Task scheduler does not exist')
            if task_scheduler.name != obj.name:
                if await task_scheduler_dao.get_by_name(db, obj.name):
                    raise errors.ConflictError(msg='Task scheduler already exists')
            if task_scheduler.type == TaskSchedulerType.CRONTAB:
                crontab_verify('m', task_scheduler.crontab_minute)
                crontab_verify('h', task_scheduler.crontab_hour)
                crontab_verify('dow', task_scheduler.crontab_day_of_week)
                crontab_verify('dom', task_scheduler.crontab_day_of_month)
                crontab_verify('moy', task_scheduler.crontab_month_of_year)
            count = await task_scheduler_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def update_status(*, pk: int) -> int:
        """
        Update task scheduler status

        :param pk: Task scheduler ID
        :return:
        """
        async with async_db_session.begin() as db:
            task_scheduler = await task_scheduler_dao.get(db, pk)
            if not task_scheduler:
                raise errors.NotFoundError(msg='Task scheduler does not exist')
            if task_scheduler.type == TaskSchedulerType.CRONTAB:
                crontab_verify('m', task_scheduler.crontab_minute)
                crontab_verify('h', task_scheduler.crontab_hour)
                crontab_verify('dow', task_scheduler.crontab_day_of_week)
                crontab_verify('dom', task_scheduler.crontab_day_of_month)
                crontab_verify('moy', task_scheduler.crontab_month_of_year)
            count = await task_scheduler_dao.set_status(db, pk, not task_scheduler.enabled)
            return count

    @staticmethod
    async def delete(*, pk) -> int:
        """
        Delete a task scheduler

        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            task_scheduler = await task_scheduler_dao.get(db, pk)
            if not task_scheduler:
                raise errors.NotFoundError(msg='Task scheduler does not exist')
            count = await task_scheduler_dao.delete(db, pk)
            return count

    @staticmethod
    async def execute(*, pk: int) -> None:
        """
        Execute a task

        :param pk: Task scheduler ID
        :return:
        """
        async with async_db_session() as db:
            workers = await run_in_threadpool(celery_app.control.ping, timeout=0.5)
            if not workers:
                raise errors.ServerError(msg='Celery Worker is temporarily unavailable, please try again later')
            task_scheduler = await task_scheduler_dao.get(db, pk)
            if not task_scheduler:
                raise errors.NotFoundError(msg='Task scheduler does not exist')
            celery_app.send_task(
                name=task_scheduler.task,
                args=json.loads(task_scheduler.args),
                kwargs=json.loads(task_scheduler.kwargs),
            )

    @staticmethod
    async def revoke(*, task_id: str) -> None:
        """
        Revoke a specified task

        :param task_id: Task UUID
        :return:
        """
        workers = await run_in_threadpool(celery_app.control.ping, timeout=0.5)
        if not workers:
            raise errors.ServerError(msg='Celery Worker is temporarily unavailable, please try again later')
        celery_app.control.revoke(task_id)


task_scheduler_service: TaskSchedulerService = TaskSchedulerService()
