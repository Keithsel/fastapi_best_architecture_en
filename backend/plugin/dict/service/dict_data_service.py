#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.dict.crud.crud_dict_data import dict_data_dao
from backend.plugin.dict.crud.crud_dict_type import dict_type_dao
from backend.plugin.dict.model import DictData
from backend.plugin.dict.schema.dict_data import CreateDictDataParam, DeleteDictDataParam, UpdateDictDataParam


class DictDataService:
    """Dictionary Data Service Class"""

    @staticmethod
    async def get(*, pk: int) -> DictData:
        """
        Get dictionary data details

        :param pk: Dictionary data ID
        :return:
        """
        async with async_db_session() as db:
            dict_data = await dict_data_dao.get(db, pk)
            if not dict_data:
                raise errors.NotFoundError(msg='Dictionary data does not exist')
            return dict_data

    @staticmethod
    async def get_all() -> Sequence[DictData]:
        async with async_db_session() as db:
            dict_datas = await dict_data_dao.get_all(db)
            return dict_datas

    @staticmethod
    async def get_select(
        *, type_code: str | None, label: str | None, value: str | None, status: int | None, type_id: int | None
    ) -> Select:
        """
        Get dictionary data list query conditions

        :param type_code: Dictionary type code
        :param label: Dictionary data label
        :param value: Dictionary data value
        :param status: Status
        :param type_id: Dictionary type ID
        :return:
        """
        return await dict_data_dao.get_list(
            type_code=type_code, label=label, value=value, status=status, type_id=type_id
        )

    @staticmethod
    async def create(*, obj: CreateDictDataParam) -> None:
        """
        Create dictionary data

        :param obj: Dictionary data creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            dict_data = await dict_data_dao.get_by_label(db, obj.label)
            if dict_data:
                raise errors.ConflictError(msg='Dictionary data already exists')
            dict_type = await dict_type_dao.get(db, obj.type_id)
            if not dict_type:
                raise errors.NotFoundError(msg='Dictionary type does not exist')
            await dict_data_dao.create(db, obj, dict_type.code)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDictDataParam) -> int:
        """
        Update dictionary data

        :param pk: Dictionary data ID
        :param obj: Dictionary data update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            dict_data = await dict_data_dao.get(db, pk)
            if not dict_data:
                raise errors.NotFoundError(msg='Dictionary data does not exist')
            if dict_data.label != obj.label:
                if await dict_data_dao.get_by_label(db, obj.label):
                    raise errors.ConflictError(msg='Dictionary data already exists')
            dict_type = await dict_type_dao.get(db, obj.type_id)
            if not dict_type:
                raise errors.NotFoundError(msg='Dictionary type does not exist')
            count = await dict_data_dao.update(db, pk, obj, dict_type.code)
            return count

    @staticmethod
    async def delete(*, obj: DeleteDictDataParam) -> int:
        """
        Batch delete dictionary data

        :param obj: Dictionary data ID list
        :return:
        """
        async with async_db_session.begin() as db:
            count = await dict_data_dao.delete(db, obj.pks)
            return count


dict_data_service: DictDataService = DictDataService()
