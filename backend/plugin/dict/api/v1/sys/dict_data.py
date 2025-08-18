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
from backend.plugin.dict.schema.dict_data import (
    CreateDictDataParam,
    DeleteDictDataParam,
    GetDictDataDetail,
    UpdateDictDataParam,
)
from backend.plugin.dict.service.dict_data_service import dict_data_service

router = APIRouter()


@router.get('/all', summary='Get all dictionary data', dependencies=[DependsJwtAuth])
async def get_all_dict_datas() -> ResponseSchemaModel[list[GetDictDataDetail]]:
    data = await dict_data_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}', summary='Get dictionary data detail', dependencies=[DependsJwtAuth])
async def get_dict_data(
    pk: Annotated[int, Path(description='Dictionary data ID')],
) -> ResponseSchemaModel[GetDictDataDetail]:
    data = await dict_data_service.get(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='Get all dictionary data with pagination',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_dict_datas_paged(
    db: CurrentSession,
    type_code: Annotated[str | None, Query(description='Dictionary type code')] = None,
    label: Annotated[str | None, Query(description='Dictionary data label')] = None,
    value: Annotated[str | None, Query(description='Dictionary data value')] = None,
    status: Annotated[int | None, Query(description='Status')] = None,
    type_id: Annotated[int | None, Query(description='Dictionary type ID')] = None,
) -> ResponseSchemaModel[PageData[GetDictDataDetail]]:
    dict_data_select = await dict_data_service.get_select(
        type_code=type_code, label=label, value=value, status=status, type_id=type_id
    )
    page_data = await paging_data(db, dict_data_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='Create dictionary data',
    dependencies=[
        Depends(RequestPermission('dict:data:add')),
        DependsRBAC,
    ],
)
async def create_dict_data(obj: CreateDictDataParam) -> ResponseModel:
    await dict_data_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='Update dictionary data',
    dependencies=[
        Depends(RequestPermission('dict:data:edit')),
        DependsRBAC,
    ],
)
async def update_dict_data(
    pk: Annotated[int, Path(description='Dictionary data ID')], obj: UpdateDictDataParam
) -> ResponseModel:
    count = await dict_data_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='Batch delete dictionary data',
    dependencies=[
        Depends(RequestPermission('dict:data:del')),
        DependsRBAC,
    ],
)
async def delete_dict_datas(obj: DeleteDictDataParam) -> ResponseModel:
    count = await dict_data_service.delete(obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
