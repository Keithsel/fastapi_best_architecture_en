#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field, field_validator

from backend.common.schema import SchemaBase
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_sqlalchemy


class GenColumnSchemaBase(SchemaBase):
    """Code Generation Model Base Schema"""

    name: str = Field(description='Column name')
    comment: str | None = Field(None, description='Column description')
    type: str = Field(description='SQLA model column type')
    default: str | None = Field(None, description='Default value')
    sort: int = Field(description='Column sort order')
    length: int = Field(description='Column length')
    is_pk: bool = Field(False, description='Is primary key')
    is_nullable: bool = Field(False, description='Is nullable')
    gen_business_id: int = Field(description='Code generation business ID')

    @field_validator('type')
    @classmethod
    def type_update(cls, v: str) -> str:
        """Update column type"""
        return sql_type_to_sqlalchemy(v)


class CreateGenColumnParam(GenColumnSchemaBase):
    """Create code generation model column parameters"""


class UpdateGenColumnParam(GenColumnSchemaBase):
    """Update code generation model column parameters"""


class GetGenColumnDetail(GenColumnSchemaBase):
    """Get code generation model column details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Primary key ID')
    pd_type: str = Field(description='Corresponding Pydantic type for the column')
