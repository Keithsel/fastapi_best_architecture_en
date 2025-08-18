#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Any, Type, TypeVar

T = TypeVar('T', bound=Enum)


class _EnumBase:
    """Enum base class, provides common methods"""

    @classmethod
    def get_member_keys(cls: Type[T]) -> list[str]:
        """Get list of enum member names"""
        return [name for name in cls.__members__.keys()]

    @classmethod
    def get_member_values(cls: Type[T]) -> list:
        """Get list of enum member values"""
        return [item.value for item in cls.__members__.values()]

    @classmethod
    def get_member_dict(cls: Type[T]) -> dict[str, Any]:
        """Get dictionary of enum members"""
        return {name: item.value for name, item in cls.__members__.items()}


class IntEnum(_EnumBase, SourceIntEnum):
    """Integer enum base class"""

    pass


class StrEnum(_EnumBase, str, Enum):
    """String enum base class"""

    pass


class MenuType(IntEnum):
    """Menu type"""

    directory = 0
    menu = 1
    button = 2
    embedded = 3
    link = 4


class RoleDataRuleOperatorType(IntEnum):
    """Data rule operator"""

    AND = 0
    OR = 1


class RoleDataRuleExpressionType(IntEnum):
    """Data rule expression"""

    eq = 0  # ==
    ne = 1  # !=
    gt = 2  # >
    ge = 3  # >=
    lt = 4  # <
    le = 5  # <=
    in_ = 6
    not_in = 7


class MethodType(StrEnum):
    """HTTP request method"""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'


class LoginLogStatusType(IntEnum):
    """Login log status"""

    fail = 0
    success = 1


class BuildTreeType(StrEnum):
    """Build tree structure type"""

    traversal = 'traversal'
    recursive = 'recursive'


class OperaLogCipherType(IntEnum):
    """Operation log encryption type"""

    aes = 0
    md5 = 1
    itsdangerous = 2
    plan = 3


class StatusType(IntEnum):
    """Status type"""

    disable = 0
    enable = 1


class UserSocialType(StrEnum):
    """User social type"""

    github = 'GitHub'
    linux_do = 'LinuxDo'


class FileType(StrEnum):
    """File type"""

    image = 'image'
    video = 'video'


class PluginType(StrEnum):
    """Plugin type"""

    zip = 'zip'
    git = 'git'


class UserPermissionType(StrEnum):
    """User permission type"""

    superuser = 'superuser'
    staff = 'staff'
    status = 'status'
    multi_login = 'multi_login'


class DataBaseType(StrEnum):
    """Database type"""

    mysql = 'mysql'
    postgresql = 'postgresql'


class PrimaryKeyType(StrEnum):
    """Primary key type"""

    autoincrement = 'autoincrement'
    snowflake = 'snowflake'
