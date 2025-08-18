#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import StreamingResponse

from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.conf import settings
from backend.plugin.code_generator.schema.code import ImportParam
from backend.plugin.code_generator.service.code_service import gen_service

router = APIRouter()


@router.get('/tables', summary='Get database tables')
async def get_all_tables(
    table_schema: Annotated[str, Query(description='Database name')] = 'fba',
) -> ResponseSchemaModel[list[dict[str, str]]]:
    data = await gen_service.get_tables(table_schema=table_schema)
    return response_base.success(data=data)


@router.post(
    '/imports',
    summary='Import code generation business and model columns',
    dependencies=[
        Depends(RequestPermission('codegen:table:import')),
        DependsRBAC,
    ],
)
async def import_table(obj: ImportParam) -> ResponseModel:
    await gen_service.import_business_and_model(obj=obj)
    return response_base.success()


@router.get('/{pk}/previews', summary='Code generation preview', dependencies=[DependsJwtAuth])
async def preview_code(pk: Annotated[int, Path(description='Business ID')]) -> ResponseSchemaModel[dict[str, bytes]]:
    data = await gen_service.preview(pk=pk)
    return response_base.success(data=data)


@router.get('/{pk}/paths', summary='Get code generation paths', dependencies=[DependsJwtAuth])
async def get_generate_paths(pk: Annotated[int, Path(description='Business ID')]) -> ResponseSchemaModel[list[str]]:
    data = await gen_service.get_generate_path(pk=pk)
    return response_base.success(data=data)


@router.post(
    '/{pk}/generation',
    summary='Code generation',
    description='File will be written to disk, please operate with caution',
    dependencies=[
        Depends(RequestPermission('codegen:local:write')),
        DependsRBAC,
    ],
)
async def generate_code(pk: Annotated[int, Path(description='Business ID')]) -> ResponseModel:
    await gen_service.generate(pk=pk)
    return response_base.success()


@router.get('/{pk}', summary='Download code', dependencies=[DependsJwtAuth])
async def download_code(pk: Annotated[int, Path(description='Business ID')]):
    bio = await gen_service.download(pk=pk)
    return StreamingResponse(
        bio,
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename={settings.CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME}.zip'},
    )
