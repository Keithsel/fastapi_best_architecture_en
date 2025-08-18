#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field
from pydantic.types import JsonValue

from backend.app.task.enums import PeriodType, TaskSchedulerType
from backend.common.schema import SchemaBase


class TaskSchedulerSchemeBase(SchemaBase):
    """Task scheduling parameters"""

    name: str = Field(description='Task name')
    task: str = Field(description='Celery task to run')
    args: JsonValue | None = Field(default=None, description='Positional arguments for the task')
    kwargs: JsonValue | None = Field(default=None, description='Keyword arguments for the task')
    queue: str | None = Field(default=None, description='Queue defined in CELERY_TASK_QUEUES')
    exchange: str | None = Field(default=None, description='Low-level AMQP routing exchange')
    routing_key: str | None = Field(default=None, description='Low-level AMQP routing key')
    start_time: datetime | None = Field(default=None, description='Time when the task starts')
    expire_time: datetime | None = Field(
        default=None, description='Deadline after which the task will not be triggered'
    )
    expire_seconds: int | None = Field(
        default=None, description='Time difference in seconds after which the task will not be triggered'
    )
    type: TaskSchedulerType = Field(description='Schedule type (0 interval, 1 crontab)')
    interval_every: int | None = Field(default=None, description='Interval period before the task runs again')
    interval_period: PeriodType | None = Field(default=None, description='Type of interval between task runs')
    crontab: str = Field(default='* * * * *', description='Crontab schedule for the task')
    one_off: bool = Field(default=False, description='Whether to run only once')
    remark: str | None = Field(default=None, description='Remarks')


class CreateTaskSchedulerParam(TaskSchedulerSchemeBase):
    """Parameters for creating a task schedule"""


class UpdateTaskSchedulerParam(TaskSchedulerSchemeBase):
    """Parameters for updating a task schedule"""


class GetTaskSchedulerDetail(TaskSchedulerSchemeBase):
    """Task schedule details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Task schedule ID')
    enabled: bool = Field(description='Whether the task is enabled')
    total_run_count: int = Field(description='Total number of runs')
    last_run_time: datetime | None = Field(None, description='Last run time')
    created_time: datetime = Field(description='Creation time')
    updated_time: datetime | None = Field(None, description='Update time')
