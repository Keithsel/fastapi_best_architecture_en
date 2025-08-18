#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.plugin.dict.model import DictType


class DictData(Base):
    """Dictionary Data Table"""

    __tablename__ = 'sys_dict_data'

    id: Mapped[id_key] = mapped_column(init=False)
    type_code: Mapped[str] = mapped_column(String(32), comment='Corresponding dictionary type code')
    label: Mapped[str] = mapped_column(String(32), comment='Dictionary label')
    value: Mapped[str] = mapped_column(String(32), comment='Dictionary value')
    sort: Mapped[int] = mapped_column(default=0, comment='Sort order')
    status: Mapped[int] = mapped_column(default=1, comment='Status (0 disabled, 1 enabled)')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Remarks'
    )

    # Dictionary type one-to-many
    type_id: Mapped[int] = mapped_column(
        ForeignKey('sys_dict_type.id', ondelete='CASCADE'), default=0, comment='Dictionary type association ID'
    )
    type: Mapped[DictType] = relationship(init=False, back_populates='datas')
