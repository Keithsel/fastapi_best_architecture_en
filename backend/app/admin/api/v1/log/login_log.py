#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.app.admin.schema.login_log import DeleteLoginLogParam, GetLoginLogDetail
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get(
    '',
    summary='Get login logs with pagination',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_login_logs_paged(
    db: CurrentSession,
    username: Annotated[str | None, Query(description='Username')] = None,
    status: Annotated[int | None, Query(description='Status')] = None,
    ip: Annotated[str | None, Query(description='IP address')] = None,
) -> ResponseSchemaModel[PageData[GetLoginLogDetail]]:
    log_select = await login_log_service.get_select(username=username, status=status, ip=ip)
    page_data = await paging_data(db, log_select)
    return response_base.success(data=page_data)


@router.delete(
    '',
    summary='Batch delete login logs',
    dependencies=[
        Depends(RequestPermission('log:login:del')),
        DependsRBAC,
    ],
)
async def delete_login_logs(obj: DeleteLoginLogParam) -> ResponseModel:
    count = await login_log_service.delete(obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/all',
    summary='Clear all login logs',
    dependencies=[
        Depends(RequestPermission('log:login:clear')),
        DependsRBAC,
    ],
)
async def delete_all_login_logs() -> ResponseModel:
    count = await login_log_service.delete_all()
    if count > 0:
        return response_base.success()
    return response_base.fail()
