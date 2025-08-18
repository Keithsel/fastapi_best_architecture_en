#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DictDataSchemaBase(SchemaBase):
    """Dictionary Data Base Model"""

    type_id: int = Field(description='Dictionary Type ID')
    label: str = Field(description='Dictionary Label')
    value: str = Field(description='Dictionary Value')
    sort: int = Field(description='Sort Order')
    status: StatusType = Field(description='Status')
    remark: str | None = Field(None, description='Remarks')


class CreateDictDataParam(DictDataSchemaBase):
    """Create Dictionary Data Parameters"""


class UpdateDictDataParam(DictDataSchemaBase):
    """Update Dictionary Data Parameters"""


class DeleteDictDataParam(SchemaBase):
    """Delete Dictionary Data Parameters"""

    pks: list[int] = Field(description='Dictionary Data ID List')


class GetDictDataDetail(DictDataSchemaBase):
    """Dictionary Data Details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Dictionary Data ID')
    type_code: str = Field(description='Dictionary Type Code')
    created_time: datetime = Field(description='Creation Time')
    updated_time: datetime | None = Field(None, description='Update Time')
