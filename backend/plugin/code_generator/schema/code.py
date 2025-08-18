#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.schema import SchemaBase


class ImportParam(SchemaBase):
    """Import Parameters"""

    app: str = Field(description='Application name, used for code generation to the specified app')
    table_schema: str = Field(description='Database name')
    table_name: str = Field(description='Database table name')
