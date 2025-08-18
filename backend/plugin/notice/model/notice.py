#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import TEXT, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Notice(Base):
    """System Notice and Announcement Table"""

    __tablename__ = 'sys_notice'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(50), comment='Title')
    type: Mapped[int] = mapped_column(comment='Type (0: Notice, 1: Announcement)')
    author: Mapped[str] = mapped_column(String(16), comment='Author')
    source: Mapped[str] = mapped_column(String(50), comment='Source')
    status: Mapped[int] = mapped_column(comment='Status (0: Hidden, 1: Visible)')
    content: Mapped[str] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='Content')
