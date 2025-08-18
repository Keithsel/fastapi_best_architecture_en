#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.plugin.code_generator.model import GenColumn


class GenBusiness(Base):
    """Code Generation Business Table"""

    __tablename__ = 'gen_business'

    id: Mapped[id_key] = mapped_column(init=False)
    app_name: Mapped[str] = mapped_column(String(50), comment='Application name (English)')
    table_name: Mapped[str] = mapped_column(String(255), unique=True, comment='Table name (English)')
    doc_comment: Mapped[str] = mapped_column(String(255), comment='Documentation comment (for function/parameter docs)')
    table_comment: Mapped[str | None] = mapped_column(String(255), default=None, comment='Table description')
    # relate_model_fk: Mapped[int | None] = mapped_column(default=None, comment='Related table foreign key')
    class_name: Mapped[str | None] = mapped_column(
        String(50), default=None, comment='Base class name (default is English table name)'
    )
    schema_name: Mapped[str | None] = mapped_column(
        String(50), default=None, comment='Schema name (default is English table name)'
    )
    filename: Mapped[str | None] = mapped_column(
        String(50), default=None, comment='Base filename (default is English table name)'
    )
    default_datetime_column: Mapped[bool] = mapped_column(default=True, comment='Has default datetime column')
    api_version: Mapped[str] = mapped_column(
        String(20), default='v1', comment='Code generation API version, default is v1'
    )
    gen_path: Mapped[str | None] = mapped_column(
        String(255), default=None, comment='Code generation path (default is app root path)'
    )
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Remarks'
    )
    # One-to-many relationship with code generation business model columns
    gen_column: Mapped[list['GenColumn']] = relationship(init=False, back_populates='gen_business')
