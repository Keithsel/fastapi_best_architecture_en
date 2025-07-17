#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.schema import SchemaBase


class DataRuleSchemaBase(SchemaBase):
    """Data Rule Base Model"""

    name: str = Field(description='Rule Name')
    model: str = Field(description='Model Name')
    column: str = Field(description='Column Name')
    operator: RoleDataRuleOperatorType = Field(RoleDataRuleOperatorType.AND, description='Operator (AND/OR)')
    expression: RoleDataRuleExpressionType = Field(RoleDataRuleExpressionType.eq, description='Expression Type')
    value: str = Field(description='Rule Value')


class CreateDataRuleParam(DataRuleSchemaBase):
    """Create Data Rule Parameters"""


class UpdateDataRuleParam(DataRuleSchemaBase):
    """Update Data Rule Parameters"""


class DeleteDataRuleParam(SchemaBase):
    """Delete Data Rule Parameters"""

    pks: list[int] = Field(description='Rule ID List')


class GetDataRuleDetail(DataRuleSchemaBase):
    """Data Rule Detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Rule ID')
    created_time: datetime = Field(description='Created Time')
    updated_time: datetime | None = Field(None, description='Updated Time')


class GetDataRuleColumnDetail(SchemaBase):
    """Available Model Field Detail for Data Rule"""

    key: str = Field(description='Field Name')
    comment: str = Field(description='Field Comment')
