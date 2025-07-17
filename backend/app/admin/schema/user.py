#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import ConfigDict, EmailStr, Field, HttpUrl, model_validator
from typing_extensions import Self

from backend.app.admin.schema.dept import GetDeptDetail
from backend.app.admin.schema.role import GetRoleWithRelationDetail
from backend.common.enums import StatusType
from backend.common.schema import CustomEmailStr, CustomPhoneNumber, SchemaBase


class AuthSchemaBase(SchemaBase):
    """User authentication base model"""

    username: str = Field(description='Username')
    password: str | None = Field(description='Password')


class AuthLoginParam(AuthSchemaBase):
    """User login parameters"""

    captcha: str = Field(description='Captcha')


class AddUserParam(AuthSchemaBase):
    """Add user parameters"""

    dept_id: int = Field(description='Department ID')
    roles: list[int] = Field(description='Role ID list')
    nickname: str | None = Field(None, description='Nickname')


class AddOAuth2UserParam(AuthSchemaBase):
    """Add OAuth2 user parameters"""

    nickname: str | None = Field(None, description='Nickname')
    email: EmailStr = Field(description='Email')
    avatar: HttpUrl | None = Field(None, description='Avatar URL')


class ResetPasswordParam(SchemaBase):
    """Reset password parameters"""

    old_password: str = Field(description='Old password')
    new_password: str = Field(description='New password')
    confirm_password: str = Field(description='Confirm password')


class UserInfoSchemaBase(SchemaBase):
    """User info base model"""

    dept_id: int | None = Field(None, description='Department ID')
    username: str = Field(description='Username')
    nickname: str = Field(description='Nickname')
    avatar: HttpUrl | None = Field(None, description='Avatar URL')


class UpdateUserParam(UserInfoSchemaBase):
    """Update user parameters"""

    roles: list[int] = Field(description='Role ID list')


class GetUserInfoDetail(UserInfoSchemaBase):
    """User info detail"""

    model_config = ConfigDict(from_attributes=True)

    dept_id: int | None = Field(None, description='Department ID')
    id: int = Field(description='User ID')
    uuid: str = Field(description='User UUID')
    email: CustomEmailStr | None = Field(None, description='Email')
    phone: CustomPhoneNumber | None = Field(None, description='Phone number')
    status: StatusType = Field(description='Status')
    is_superuser: bool = Field(description='Is superuser')
    is_staff: bool = Field(description='Is admin')
    is_multi_login: bool = Field(description='Allow multi-terminal login')
    join_time: datetime = Field(description='Join time')
    last_login_time: datetime | None = Field(None, description='Last login time')


class GetUserInfoWithRelationDetail(GetUserInfoDetail):
    """User info with relation detail"""

    model_config = ConfigDict(from_attributes=True)

    dept: GetDeptDetail | None = Field(None, description='Department info')
    roles: list[GetRoleWithRelationDetail] = Field(description='Role list')


class GetCurrentUserInfoWithRelationDetail(GetUserInfoWithRelationDetail):
    """Current user info with relation detail"""

    model_config = ConfigDict(from_attributes=True)

    dept: str | None = Field(None, description='Department name')
    roles: list[str] = Field(description='Role name list')

    @model_validator(mode='before')
    @classmethod
    def handel(cls, data: Any) -> Self:
        """Process department and role data"""
        dept = data['dept']
        if dept:
            data['dept'] = dept['name']
        roles = data['roles']
        if roles:
            data['roles'] = [role['name'] for role in roles]
        return data
