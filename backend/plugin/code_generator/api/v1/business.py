#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession
from backend.plugin.code_generator.schema.business import (
    CreateGenBusinessParam,
    GetGenBusinessDetail,
    UpdateGenBusinessParam,
)
from backend.plugin.code_generator.schema.column import GetGenColumnDetail
from backend.plugin.code_generator.service.business_service import gen_business_service
from backend.plugin.code_generator.service.column_service import gen_column_service

router = APIRouter()


@router.get('/all', summary='Get all code generation businesses', dependencies=[DependsJwtAuth])
async def get_all_businesses() -> ResponseSchemaModel[list[GetGenBusinessDetail]]:
    data = await gen_business_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}', summary='Get code generation business details', dependencies=[DependsJwtAuth])
async def get_business(
    pk: Annotated[int, Path(description='Business ID')],
) -> ResponseSchemaModel[GetGenBusinessDetail]:
    data = await gen_business_service.get(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='Get all code generation businesses with pagination',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_businesses_paged(
    db: CurrentSession,
    table_name: Annotated[str | None, Query(description='Code generation business table name')] = None,
) -> ResponseSchemaModel[PageData[GetGenBusinessDetail]]:
    business_select = await gen_business_service.get_select(table_name=table_name)
    page_data = await paging_data(db, business_select)
    return response_base.success(data=page_data)


@router.get(
    '/{pk}/columns', summary='Get all model columns for a code generation business', dependencies=[DependsJwtAuth]
)
async def get_business_all_columns(
    pk: Annotated[int, Path(description='Business ID')],
) -> ResponseSchemaModel[list[GetGenColumnDetail]]:
    data = await gen_column_service.get_columns(business_id=pk)
    return response_base.success(data=data)


@router.post(
    '',
    summary='Create code generation business',
    deprecated=True,
    dependencies=[
        Depends(RequestPermission('codegen:business:add')),
        DependsRBAC,
    ],
)
async def create_business(obj: CreateGenBusinessParam) -> ResponseModel:
    await gen_business_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='Update code generation business',
    dependencies=[
        Depends(RequestPermission('codegen:business:edit')),
        DependsRBAC,
    ],
)
async def update_business(
    pk: Annotated[int, Path(description='Business ID')], obj: UpdateGenBusinessParam
) -> ResponseModel:
    count = await gen_business_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='Delete code generation business',
    dependencies=[
        Depends(RequestPermission('codegen:business:del')),
        DependsRBAC,
    ],
)
async def delete_business(pk: Annotated[int, Path(description='Business ID')]) -> ResponseModel:
    count = await gen_business_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
