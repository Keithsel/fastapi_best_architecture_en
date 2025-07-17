#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_rule import GetDataRuleDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DataScopeBase(SchemaBase):
    """Data Scope Base Model"""

    name: str = Field(description='Name')
    status: StatusType = Field(StatusType.enable, description='Status')


class CreateDataScopeParam(DataScopeBase):
    """Create Data Scope Parameters"""


class UpdateDataScopeParam(DataScopeBase):
    """Update Data Scope Parameters"""


class UpdateDataScopeRuleParam(SchemaBase):
    """Update Data Scope Rule Parameters"""

    rules: list[int] = Field(description='Data Rule ID List')


class DeleteDataScopeParam(SchemaBase):
    """Delete Data Scope Parameters"""

    pks: list[int] = Field(description='Data Scope ID List')


class GetDataScopeDetail(DataScopeBase):
    """Data Scope Detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Data Scope ID')
    created_time: datetime = Field(description='Created Time')
    updated_time: datetime | None = Field(None, description='Updated Time')


class GetDataScopeWithRelationDetail(GetDataScopeDetail):
    """Data Scope With Relation Detail"""

    rules: list[GetDataRuleDetail] = Field([], description='Data Rule List')
