#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Union

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import DataClassBase, id_key

if TYPE_CHECKING:
    from backend.plugin.code_generator.model import GenBusiness


class GenColumn(DataClassBase):
    """Code Generation Model Column Table"""

    __tablename__ = 'gen_column'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='Column name')
    comment: Mapped[str | None] = mapped_column(String(255), default=None, comment='Column description')
    type: Mapped[str] = mapped_column(String(20), default='String', comment='SQLA model column type')
    pd_type: Mapped[str] = mapped_column(String(20), default='str', comment='Corresponding Pydantic type')
    default: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Default value'
    )
    sort: Mapped[int | None] = mapped_column(default=1, comment='Column sort order')
    length: Mapped[int] = mapped_column(default=0, comment='Column length')
    is_pk: Mapped[bool] = mapped_column(default=False, comment='Is primary key')
    is_nullable: Mapped[bool] = mapped_column(default=False, comment='Is nullable')

    # One-to-many relationship with code generation business model
    gen_business_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('gen_business.id', ondelete='CASCADE'), default=0, comment='Code generation business ID'
    )
    gen_business: Mapped[Union['GenBusiness', None]] = relationship(init=False, back_populates='gen_column')
