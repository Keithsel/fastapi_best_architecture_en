#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_scope import GetDataScopeDetail
from backend.app.admin.schema.menu import GetMenuDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class RoleSchemaBase(SchemaBase):
    """Role Base Model"""

    name: str = Field(description='Role Name')
    status: StatusType = Field(description='Status')
    is_filter_scopes: bool = Field(True, description='Filter Data Permissions')
    remark: str | None = Field(None, description='Remark')


class CreateRoleParam(RoleSchemaBase):
    """Create Role Parameters"""


class UpdateRoleParam(RoleSchemaBase):
    """Update Role Parameters"""


class DeleteRoleParam(SchemaBase):
    """Delete Role Parameters"""

    pks: list[int] = Field(description='Role ID List')


class UpdateRoleMenuParam(SchemaBase):
    """Update Role Menu Parameters"""

    menus: list[int] = Field(description='Menu ID List')


class UpdateRoleScopeParam(SchemaBase):
    """Update Role Data Scope Parameters"""

    scopes: list[int] = Field(description='Data Scope ID List')


class GetRoleDetail(RoleSchemaBase):
    """Role Detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Role ID')
    created_time: datetime = Field(description='Created Time')
    updated_time: datetime | None = Field(None, description='Updated Time')


class GetRoleWithRelationDetail(GetRoleDetail):
    """Role Relation Detail"""

    menus: list[GetMenuDetail | None] = Field([], description='Menu Detail List')
    scopes: list[GetDataScopeDetail | None] = Field([], description='Data Scope List')
