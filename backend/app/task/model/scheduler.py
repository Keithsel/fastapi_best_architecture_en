#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    String,
    event,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import INTEGER, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.exception import errors
from backend.common.model import Base, TimeZone, id_key
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.timezone import timezone


class TaskScheduler(Base):
    """Task scheduling table"""

    __tablename__ = 'task_scheduler'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='Task Name')
    task: Mapped[str] = mapped_column(String(255), comment='Celery Task to Run')
    args: Mapped[str | None] = mapped_column(JSON(), comment='Positional Arguments for the Task')
    kwargs: Mapped[str | None] = mapped_column(JSON(), comment='Keyword Arguments for the Task')
    queue: Mapped[str | None] = mapped_column(String(255), comment='Queue Defined in CELERY_TASK_QUEUES')
    exchange: Mapped[str | None] = mapped_column(String(255), comment='Low-level AMQP Routing Exchange')
    routing_key: Mapped[str | None] = mapped_column(String(255), comment='Low-level AMQP Routing Key')
    start_time: Mapped[datetime | None] = mapped_column(TimeZone, comment='Task Start Trigger Time')
    expire_time: Mapped[datetime | None] = mapped_column(TimeZone, comment='Task Expiry Time')
    expire_seconds: Mapped[int | None] = mapped_column(comment='Time Difference in Seconds Until Task Expires')
    type: Mapped[int] = mapped_column(comment='Schedule Type (0 Interval, 1 Crontab)')
    interval_every: Mapped[int | None] = mapped_column(comment='Interval Period Before Task Runs Again')
    interval_period: Mapped[str | None] = mapped_column(String(255), comment='Type of Interval Between Runs')
    crontab: Mapped[str | None] = mapped_column(String(50), default='* * * * *', comment='Crontab Schedule for Task')
    one_off: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=False, comment='Whether to Run Only Once'
    )
    enabled: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=True, comment='Whether the Task is Enabled'
    )
    total_run_count: Mapped[int] = mapped_column(default=0, comment='Total Number of Times Task Triggered')
    last_run_time: Mapped[datetime | None] = mapped_column(TimeZone, default=None, comment='Last Time Task Was Triggered')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Remarks'
    )

    no_changes: bool = False

    @staticmethod
    def before_insert_or_update(mapper, connection, target):
        if target.expire_seconds is not None and target.expire_time:
            raise errors.ConflictError(msg='Only one of expire_time and expire_seconds can be set')

    @classmethod
    def changed(cls, mapper, connection, target):
        if not target.no_changes:
            cls.update_changed(mapper, connection, target)

    @classmethod
    async def update_changed_async(cls):
        now = timezone.now()
        await redis_client.set(f'{settings.CELERY_REDIS_PREFIX}:last_update', timezone.to_str(now))

    @classmethod
    def update_changed(cls, mapper, connection, target):
        asyncio.create_task(cls.update_changed_async())


# Event listeners
event.listen(TaskScheduler, 'before_insert', TaskScheduler.before_insert_or_update)
event.listen(TaskScheduler, 'before_update', TaskScheduler.before_insert_or_update)
event.listen(TaskScheduler, 'after_insert', TaskScheduler.update_changed)
event.listen(TaskScheduler, 'after_delete', TaskScheduler.update_changed)
event.listen(TaskScheduler, 'after_update', TaskScheduler.changed)
