#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import HTTPBasicCredentials
from fastapi_limiter.depends import RateLimiter
from starlette.background import BackgroundTasks

from backend.app.admin.schema.token import GetLoginToken, GetNewToken, GetSwaggerToken
from backend.app.admin.schema.user import AuthLoginParam
from backend.app.admin.service.auth_service import auth_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.post('/login/swagger', summary='For Swagger Debugging', description='Quickly obtain a token for Swagger authentication')
async def login_swagger(obj: Annotated[HTTPBasicCredentials, Depends()]) -> GetSwaggerToken:
    token, user = await auth_service.swagger_login(obj=obj)
    return GetSwaggerToken(access_token=token, user=user)


@router.post(
    '/login',
    summary='User Login',
    description='Login in JSON format, only supported for debugging with third-party API tools, e.g., Postman',
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def login(
    request: Request, response: Response, obj: AuthLoginParam, background_tasks: BackgroundTasks
) -> ResponseSchemaModel[GetLoginToken]:
    data = await auth_service.login(request=request, response=response, obj=obj, background_tasks=background_tasks)
    return response_base.success(data=data)


@router.get('/codes', summary='Get All Authorization Codes', description='Compatible with vben admin v5', dependencies=[DependsJwtAuth])
async def get_codes(request: Request) -> ResponseSchemaModel[list[str]]:
    codes = await auth_service.get_codes(request=request)
    return response_base.success(data=codes)


@router.post('/tokens', summary='Refresh Token')
async def refresh_token(request: Request) -> ResponseSchemaModel[GetNewToken]:
    data = await auth_service.refresh_token(request=request)
    return response_base.success(data=data)


@router.post('/logout', summary='User Logout')
async def logout(request: Request, response: Response) -> ResponseModel:
    await auth_service.logout(request=request, response=response)
    return response_base.success()
