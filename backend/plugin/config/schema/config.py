#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ConfigSchemaBase(SchemaBase):
    """Configuration parameter base model"""

    name: str = Field(description='Configuration parameter name')
    type: str | None = Field(None, description='Configuration parameter type')
    key: str = Field(description='Configuration parameter key')
    value: str = Field(description='Configuration parameter value')
    is_frontend: bool = Field(description='Is frontend configuration parameter')
    remark: str | None = Field(None, description='Remark')


class CreateConfigParam(ConfigSchemaBase):
    """Create configuration parameter"""


class UpdateConfigParam(ConfigSchemaBase):
    """Update configuration parameter"""


class GetConfigDetail(ConfigSchemaBase):
    """Configuration parameter detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Configuration parameter ID')
    created_time: datetime = Field(description='Creation time')
    updated_time: datetime | None = Field(None, description='Update time')
