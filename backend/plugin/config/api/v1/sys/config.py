#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query

from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession
from backend.plugin.config.schema.config import (
    CreateConfigParam,
    GetConfigDetail,
    UpdateConfigParam,
)
from backend.plugin.config.service.config_service import config_service

router = APIRouter()


@router.get('/{pk}', summary='Get config detail', dependencies=[DependsJwtAuth])
async def get_config(pk: Annotated[int, Path(description='Config ID')]) -> ResponseSchemaModel[GetConfigDetail]:
    config = await config_service.get(pk=pk)
    return response_base.success(data=config)


@router.get(
    '',
    summary='Get all configs with pagination',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_configs_paged(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='Config name')] = None,
    type: Annotated[str | None, Query(description='Config type')] = None,
) -> ResponseSchemaModel[PageData[GetConfigDetail]]:
    config_select = await config_service.get_select(name=name, type=type)
    page_data = await paging_data(db, config_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='Create config',
    dependencies=[
        Depends(RequestPermission('sys:config:add')),
        DependsRBAC,
    ],
)
async def create_config(obj: CreateConfigParam) -> ResponseModel:
    await config_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='Update config',
    dependencies=[
        Depends(RequestPermission('sys:config:edit')),
        DependsRBAC,
    ],
)
async def update_config(pk: Annotated[int, Path(description='Config ID')], obj: UpdateConfigParam) -> ResponseModel:
    count = await config_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='Batch delete configs',
    dependencies=[
        Depends(RequestPermission('sys:config:del')),
        DependsRBAC,
    ],
)
async def delete_configs(pks: Annotated[list[int], Body(description='Config ID list')]) -> ResponseModel:
    count = await config_service.delete(pks=pks)
    if count > 0:
        return response_base.success()
    return response_base.fail()
