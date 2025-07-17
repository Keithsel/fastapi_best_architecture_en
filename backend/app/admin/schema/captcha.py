#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.schema import SchemaBase


class GetCaptchaDetail(SchemaBase):
    """Captcha Detail"""

    image_type: str = Field(description='Image type')
    image: str = Field(description='Image content')
