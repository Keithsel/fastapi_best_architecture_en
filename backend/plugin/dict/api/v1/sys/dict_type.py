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
from backend.plugin.dict.schema.dict_type import (
    CreateDictTypeParam,
    DeleteDictTypeParam,
    GetDictTypeDetail,
    UpdateDictTypeParam,
)
from backend.plugin.dict.service.dict_type_service import dict_type_service

router = APIRouter()


@router.get('/{pk}', summary='Get dictionary type detail', dependencies=[DependsJwtAuth])
async def get_dict_type(
    pk: Annotated[int, Path(description='Dictionary type ID')],
) -> ResponseSchemaModel[GetDictTypeDetail]:
    data = await dict_type_service.get(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='Get all dictionary types with pagination',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_dict_types_paged(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='Dictionary type name')] = None,
    code: Annotated[str | None, Query(description='Dictionary type code')] = None,
    status: Annotated[int | None, Query(description='Status')] = None,
) -> ResponseSchemaModel[PageData[GetDictTypeDetail]]:
    dict_type_select = await dict_type_service.get_select(name=name, code=code, status=status)
    page_data = await paging_data(db, dict_type_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='Create dictionary type',
    dependencies=[
        Depends(RequestPermission('dict:type:add')),
        DependsRBAC,
    ],
)
async def create_dict_type(obj: CreateDictTypeParam) -> ResponseModel:
    await dict_type_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='Update dictionary type',
    dependencies=[
        Depends(RequestPermission('dict:type:edit')),
        DependsRBAC,
    ],
)
async def update_dict_type(
    pk: Annotated[int, Path(description='Dictionary type ID')], obj: UpdateDictTypeParam
) -> ResponseModel:
    count = await dict_type_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='Batch delete dictionary types',
    dependencies=[
        Depends(RequestPermission('dict:type:del')),
        DependsRBAC,
    ],
)
async def delete_dict_types(obj: DeleteDictTypeParam) -> ResponseModel:
    count = await dict_type_service.delete(obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
