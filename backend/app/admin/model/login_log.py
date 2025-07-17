#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key
from backend.utils.timezone import timezone


class LoginLog(DataClassBase):
    """Login Log Table"""

    __tablename__ = 'sys_login_log'

    id: Mapped[id_key] = mapped_column(init=False)
    user_uuid: Mapped[str] = mapped_column(String(50), comment='User UUID')
    username: Mapped[str] = mapped_column(String(20), comment='Username')
    status: Mapped[int] = mapped_column(insert_default=0, comment='Login Status (0 Failed 1 Success)')
    ip: Mapped[str] = mapped_column(String(50), comment='Login IP Address')
    country: Mapped[str | None] = mapped_column(String(50), comment='Country')
    region: Mapped[str | None] = mapped_column(String(50), comment='Region')
    city: Mapped[str | None] = mapped_column(String(50), comment='City')
    user_agent: Mapped[str] = mapped_column(String(255), comment='User Agent')
    os: Mapped[str | None] = mapped_column(String(50), comment='Operating System')
    browser: Mapped[str | None] = mapped_column(String(50), comment='Browser')
    device: Mapped[str | None] = mapped_column(String(50), comment='Device')
    msg: Mapped[str] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='Message')
    login_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment='Login Time')
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=timezone.now, comment='Created Time'
    )
