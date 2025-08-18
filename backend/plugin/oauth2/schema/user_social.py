#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.enums import UserSocialType
from backend.common.schema import SchemaBase


class UserSocialSchemaBase(SchemaBase):
    """User social base model"""

    sid: str = Field(description='Third-party user ID')
    source: UserSocialType = Field(description='Social platform')


class CreateUserSocialParam(UserSocialSchemaBase):
    """Parameters for creating user social"""

    user_id: int = Field(description='User ID')


class UpdateUserSocialParam(SchemaBase):
    """Parameters for updating user social"""
