#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field, field_serializer

from backend.app.task import celery_app
from backend.common.schema import SchemaBase


class TaskResultSchemaBase(SchemaBase):
    """Base model for task result"""

    task_id: str = Field(description='Task ID')
    status: str = Field(description='Execution status')
    result: Any | None = Field(description='Execution result')
    date_done: datetime | None = Field(description='Completion time')
    traceback: str | None = Field(description='Error traceback')
    name: str | None = Field(description='Task name')
    args: bytes | None = Field(description='Task positional arguments')
    kwargs: bytes | None = Field(description='Task keyword arguments')
    worker: str | None = Field(description='Running worker')
    retries: int | None = Field(description='Retry count')
    queue: str | None = Field(description='Running queue')


class DeleteTaskResultParam(SchemaBase):
    """Parameters for deleting task results"""

    pks: list[int] = Field(description='Task result ID list')


class GetTaskResultDetail(TaskResultSchemaBase):
    """Task result details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Task result ID')

    @field_serializer('args', 'kwargs', when_used='unless-none')
    def serialize_params(self, value: bytes | None, _info) -> Any:
        return celery_app.backend.decode(value)
