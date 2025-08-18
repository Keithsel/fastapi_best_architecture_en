#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import User


class Dept(Base):
    """Department Table"""

    __tablename__ = 'sys_dept'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='Department Name')
    sort: Mapped[int] = mapped_column(default=0, comment='Sort Order')
    leader: Mapped[str | None] = mapped_column(String(20), default=None, comment='Leader')
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='Phone')
    email: Mapped[str | None] = mapped_column(String(50), default=None, comment='Email')
    status: Mapped[int] = mapped_column(default=1, comment='Department Status (0 Disabled 1 Active)')
    del_flag: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=False, comment='Delete Flag (0 Deleted 1 Exists)'
    )

    # Parent department one-to-many
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey('sys_dept.id', ondelete='SET NULL'),
        default=None,
        index=True,
        comment='Parent Department ID',
    )
    parent: Mapped[Optional['Dept']] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[Optional[list['Dept']]] = relationship(init=False, back_populates='parent')

    # Department users one-to-many
    users: Mapped[list[User]] = relationship(init=False, back_populates='dept')
