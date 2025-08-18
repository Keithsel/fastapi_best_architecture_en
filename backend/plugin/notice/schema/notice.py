#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class NoticeSchemaBase(SchemaBase):
    """Notice and Announcement Base Model"""

    title: str = Field(description='Title')
    type: int = Field(description='Type (0: Notice, 1: Announcement)')
    author: str = Field(description='Author')
    source: str = Field(description='Source')
    status: StatusType = Field(description='Status (0: Hidden, 1: Visible)')
    content: str = Field(description='Content')


class CreateNoticeParam(NoticeSchemaBase):
    """Create Notice and Announcement Parameters"""


class UpdateNoticeParam(NoticeSchemaBase):
    """Update Notice and Announcement Parameters"""


class DeleteNoticeParam(SchemaBase):
    """Delete Notice and Announcement Parameters"""

    pks: list[int] = Field(description='Notice and Announcement ID List')


class GetNoticeDetail(NoticeSchemaBase):
    """Notice and Announcement Details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Notice and Announcement ID')
    created_time: datetime = Field(description='Creation Time')
    updated_time: datetime | None = Field(None, description='Update Time')
