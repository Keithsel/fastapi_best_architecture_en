#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import CustomEmailStr, CustomPhoneNumber, SchemaBase


class DeptSchemaBase(SchemaBase):
    """Department Base Model"""

    name: str = Field(description='Department Name')
    parent_id: int | None = Field(None, description='Parent Department ID')
    sort: int = Field(0, ge=0, description='Sort Order')
    leader: str | None = Field(None, description='Leader')
    phone: CustomPhoneNumber | None = Field(None, description='Contact Phone')
    email: CustomEmailStr | None = Field(None, description='Email')
    status: StatusType = Field(StatusType.enable, description='Status')


class CreateDeptParam(DeptSchemaBase):
    """Create Department Parameters"""


class UpdateDeptParam(DeptSchemaBase):
    """Update Department Parameters"""


class GetDeptDetail(DeptSchemaBase):
    """Department Detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Department ID')
    del_flag: bool = Field(description='Deleted')
    created_time: datetime = Field(description='Created Time')
    updated_time: datetime | None = Field(None, description='Updated Time')
