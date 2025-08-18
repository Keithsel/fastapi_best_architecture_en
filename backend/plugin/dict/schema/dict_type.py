#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DictTypeSchemaBase(SchemaBase):
    """Dictionary Type Base Model"""

    name: str = Field(description='Dictionary Name')
    code: str = Field(description='Dictionary Code')
    status: StatusType = Field(description='Status')
    remark: str | None = Field(None, description='Remarks')


class CreateDictTypeParam(DictTypeSchemaBase):
    """Create Dictionary Type Parameters"""


class UpdateDictTypeParam(DictTypeSchemaBase):
    """Update Dictionary Type Parameters"""


class DeleteDictTypeParam(SchemaBase):
    """Delete Dictionary Type Parameters"""

    pks: list[int] = Field(description='Dictionary Type ID List')


class GetDictTypeDetail(DictTypeSchemaBase):
    """Dictionary Type Details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Dictionary Type ID')
    created_time: datetime = Field(description='Creation Time')
    updated_time: datetime | None = Field(None, description='Update Time')
