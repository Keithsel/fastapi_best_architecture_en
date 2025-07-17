#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fast_captcha import img_captcha
from fastapi import APIRouter, Depends, Request
from fastapi_limiter.depends import RateLimiter
from starlette.concurrency import run_in_threadpool

from backend.app.admin.schema.captcha import GetCaptchaDetail
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.core.conf import settings
from backend.database.redis import redis_client

router = APIRouter()


@router.get(
    '/captcha',
    summary='Get login captcha',
    dependencies=[Depends(RateLimiter(times=5, seconds=10))],
)
async def get_captcha(request: Request) -> ResponseSchemaModel[GetCaptchaDetail]:
    """
    This endpoint may have performance overhead. Although it is an async endpoint,
    captcha generation is an IO-intensive task, so a thread pool is used to minimize performance loss.
    """
    img_type: str = 'base64'
    img, code = await run_in_threadpool(img_captcha, img_byte=img_type)
    ip = request.state.ip
    await redis_client.set(
        f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{ip}',
        code,
        ex=settings.CAPTCHA_LOGIN_EXPIRE_SECONDS,
    )
    data = GetCaptchaDetail(image_type=img_type, image=img)
    return response_base.success(data=data)
