#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_data_rule import data_rule_dao
from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import (
    CreateDataRuleParam,
    DeleteDataRuleParam,
    GetDataRuleColumnDetail,
    UpdateDataRuleParam,
)
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.utils.import_parse import dynamic_import_data_model


class DataRuleService:
    """Data Rule Service Class"""

    @staticmethod
    async def get(*, pk: int) -> DataRule:
        """
        Get data rule details

        :param pk: Rule ID
        :return:
        """
        async with async_db_session() as db:
            data_rule = await data_rule_dao.get(db, pk)
            if not data_rule:
                raise errors.NotFoundError(msg='Data rule does not exist')
            return data_rule

    @staticmethod
    async def get_models() -> list[str]:
        """Get all available models for data rules"""
        return list(settings.DATA_PERMISSION_MODELS.keys())

    @staticmethod
    async def get_columns(model: str) -> list[GetDataRuleColumnDetail]:
        """
        Get the list of fields for the available model of data rules

        :param model: Model name
        :return:
        """
        if model not in settings.DATA_PERMISSION_MODELS:
            raise errors.NotFoundError(msg='Available model for data rule does not exist')
        model_ins = dynamic_import_data_model(settings.DATA_PERMISSION_MODELS[model])

        model_columns = [
            GetDataRuleColumnDetail(key=column.key, comment=column.comment)
            for column in model_ins.__table__.columns
            if column.key not in settings.DATA_PERMISSION_COLUMN_EXCLUDE
        ]
        return model_columns

    @staticmethod
    async def get_select(*, name: str | None) -> Select:
        """
        Get query conditions for data rule list

        :param name: Rule name
        :return:
        """
        return await data_rule_dao.get_list(name=name)

    @staticmethod
    async def get_all() -> Sequence[DataRule]:
        """Get all data rules"""
        async with async_db_session() as db:
            data_rules = await data_rule_dao.get_all(db)
            return data_rules

    @staticmethod
    async def create(*, obj: CreateDataRuleParam) -> None:
        """
        Create data rule

        :param obj: Data rule creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            data_rule = await data_rule_dao.get_by_name(db, obj.name)
            if data_rule:
                raise errors.ConflictError(msg='Data rule already exists')
            await data_rule_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDataRuleParam) -> int:
        """
        Update data rule

        :param pk: Rule ID
        :param obj: Data rule update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            data_rule = await data_rule_dao.get(db, pk)
            if not data_rule:
                raise errors.NotFoundError(msg='Data rule does not exist')
            if data_rule.name != obj.name:
                if await data_rule_dao.get_by_name(db, obj.name):
                    raise errors.ConflictError(msg='Data rule already exists')
            count = await data_rule_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, obj: DeleteDataRuleParam) -> int:
        """
        Batch delete data rules

        :param obj: List of rule IDs
        :return:
        """
        async with async_db_session.begin() as db:
            count = await data_rule_dao.delete(db, obj.pks)
            return count


data_rule_service: DataRuleService = DataRuleService()
