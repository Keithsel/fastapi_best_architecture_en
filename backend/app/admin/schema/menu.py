#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import MenuType, StatusType
from backend.common.schema import SchemaBase


class MenuSchemaBase(SchemaBase):
    """Menu Base Model"""

    title: str = Field(description='Menu Title')
    name: str = Field(description='Menu Name')
    path: str | None = Field(None, description='Route Path')
    parent_id: int | None = Field(None, description='Parent Menu ID')
    sort: int = Field(0, ge=0, description='Sort Order')
    icon: str | None = Field(None, description='Icon')
    type: MenuType = Field(description='Menu Type (0 Directory, 1 Menu, 2 Button, 3 Embedded, 4 External Link)')
    component: str | None = Field(None, description='Component Path')
    perms: str | None = Field(None, description='Permission Identifier')
    status: StatusType = Field(description='Status')
    display: StatusType = Field(description='Display')
    cache: StatusType = Field(description='Cache')
    link: str | None = Field(None, description='External Link Address')
    remark: str | None = Field(None, description='Remark')


class CreateMenuParam(MenuSchemaBase):
    """Create Menu Parameters"""


class UpdateMenuParam(MenuSchemaBase):
    """Update Menu Parameters"""


class GetMenuDetail(MenuSchemaBase):
    """Menu Detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Menu ID')
    created_time: datetime = Field(description='Created Time')
    updated_time: datetime | None = Field(None, description='Updated Time')
