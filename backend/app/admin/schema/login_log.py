#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class LoginLogSchemaBase(SchemaBase):
    """Login Log Base Model"""

    user_uuid: str = Field(description='User UUID')
    username: str = Field(description='Username')
    status: int = Field(description='Login Status')
    ip: str = Field(description='IP Address')
    country: str | None = Field(None, description='Country')
    region: str | None = Field(None, description='Region')
    city: str | None = Field(None, description='City')
    user_agent: str = Field(description='User Agent')
    browser: str | None = Field(None, description='Browser')
    os: str | None = Field(None, description='Operating System')
    device: str | None = Field(None, description='Device')
    msg: str = Field(description='Message')
    login_time: datetime = Field(description='Login Time')


class CreateLoginLogParam(LoginLogSchemaBase):
    """Create Login Log Parameters"""


class UpdateLoginLogParam(LoginLogSchemaBase):
    """Update Login Log Parameters"""


class DeleteLoginLogParam(SchemaBase):
    """Delete Login Log Parameters"""

    pks: list[int] = Field(description='Login Log ID List')


class GetLoginLogDetail(LoginLogSchemaBase):
    """Login Log Detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Log ID')
    created_time: datetime = Field(description='Created Time')
