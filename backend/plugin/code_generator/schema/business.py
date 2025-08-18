#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    """Code Generation Business Base Model"""

    app_name: str = Field(description='Application name (English)')
    table_name: str = Field(description='Table name (English)')
    doc_comment: str = Field(description='Doc comment (used for function/parameter docs)')
    table_comment: str | None = Field(None, description='Table description')
    class_name: str | None = Field(None, description='Base class name for Python code')
    schema_name: str | None = Field(None, description='Base class name for Python Schema code')
    filename: str | None = Field(None, description='Base filename for Python code')
    default_datetime_column: bool = Field(True, description='Has default datetime columns')
    api_version: str = Field('v1', description='Code generation API version')
    gen_path: str | None = Field(None, description='Code generation path')
    remark: str | None = Field(None, description='Remarks')


class CreateGenBusinessParam(GenBusinessSchemaBase):
    """Create Code Generation Business Parameters"""


class UpdateGenBusinessParam(GenBusinessSchemaBase):
    """Update Code Generation Business Parameters"""


class GetGenBusinessDetail(GenBusinessSchemaBase):
    """Get Code Generation Business Details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Primary Key ID')
    created_time: datetime = Field(description='Creation Time')
    updated_time: datetime | None = Field(None, description='Update Time')
