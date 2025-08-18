#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from typing import Annotated

from fastapi import APIRouter, Body, Request

from backend.common.response.response_schema import response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.core.conf import settings
from backend.database.db import CurrentSession
from backend.database.redis import redis_client
from backend.plugin.email.utils.send import send_email

router = APIRouter()


@router.post('/captcha', summary='Send email captcha', dependencies=[DependsJwtAuth])
async def send_email_captcha(
    request: Request,
    db: CurrentSession,
    recipients: Annotated[str | list[str], Body(embed=True, description='Email recipients')],
):
    code = ''.join([str(random.randint(1, 9)) for _ in range(6)])
    ip = request.state.ip
    await redis_client.set(
        f'{settings.EMAIL_CAPTCHA_REDIS_PREFIX}:{ip}',
        code,
        ex=settings.EMAIL_CAPTCHA_EXPIRE_SECONDS,
    )
    content = {'code': code, 'expired': int(settings.EMAIL_CAPTCHA_EXPIRE_SECONDS / 60)}
    await send_email(db, recipients, 'FBA Captcha', content, 'captcha.html')
    return response_base.success()
