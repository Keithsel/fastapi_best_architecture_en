#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class OperaLogSchemaBase(SchemaBase):
    """Operation Log Base Model"""

    trace_id: str = Field(description='Trace ID')
    username: str | None = Field(None, description='Username')
    method: str = Field(description='Request Method')
    title: str = Field(description='Operation Title')
    path: str = Field(description='Request Path')
    ip: str = Field(description='IP Address')
    country: str | None = Field(None, description='Country')
    region: str | None = Field(None, description='Region')
    city: str | None = Field(None, description='City')
    user_agent: str = Field(description='User Agent')
    os: str | None = Field(None, description='Operating System')
    browser: str | None = Field(None, description='Browser')
    device: str | None = Field(None, description='Device')
    args: dict[str, Any] | None = Field(None, description='Request Parameters')
    status: StatusType = Field(StatusType.enable, description='Status')
    code: str = Field(description='Status Code')
    msg: str | None = Field(None, description='Message')
    cost_time: float = Field(description='Elapsed Time')
    opera_time: datetime = Field(description='Operation Time')


class CreateOperaLogParam(OperaLogSchemaBase):
    """Create Operation Log Parameters"""


class UpdateOperaLogParam(OperaLogSchemaBase):
    """Update Operation Log Parameters"""


class DeleteOperaLogParam(SchemaBase):
    """Delete Operation Log Parameters"""

    pks: list[int] = Field(description='Operation Log ID List')


class GetOperaLogDetail(OperaLogSchemaBase):
    """Operation Log Detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Log ID')
    created_time: datetime = Field(description='Created Time')
