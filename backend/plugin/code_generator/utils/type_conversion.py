#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.core.conf import settings
from backend.plugin.code_generator.enums import GenMySQLColumnType, GenPostgreSQLColumnType


def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    Convert SQL type to SQLAlchemy type

    :param typing: SQL type string
    :return:
    """
    if settings.DATABASE_TYPE == 'mysql':
        if typing in GenMySQLColumnType.get_member_keys():
            return typing
    else:
        if typing in GenPostgreSQLColumnType.get_member_keys():
            return typing
    return 'String'


def sql_type_to_pydantic(typing: str) -> str:
    """
    Convert SQL type to Pydantic type

    :param typing: SQL type string
    :return:
    """
    try:
        if settings.DATABASE_TYPE == 'mysql':
            return GenMySQLColumnType[typing].value
        if typing == 'CHARACTER VARYING':  # Alias for VARCHAR in PostgreSQL DDL
            return 'str'
        return GenPostgreSQLColumnType[typing].value
    except KeyError:
        return 'str'
