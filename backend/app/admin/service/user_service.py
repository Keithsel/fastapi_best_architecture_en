#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from typing import Sequence

from fastapi import Request
from sqlalchemy import Select

from backend.app.admin.crud.crud_dept import dept_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.model import Role, User
from backend.app.admin.schema.user import (
    AddUserParam,
    ResetPasswordParam,
    UpdateUserParam,
)
from backend.common.enums import UserPermissionType
from backend.common.exception import errors
from backend.common.security.jwt import get_hash_password, get_token, jwt_decode, password_verify, superuser_verify
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client


class UserService:
    """User Service Class"""

    @staticmethod
    async def get_userinfo(*, pk: int | None = None, username: str | None = None) -> User:
        """
        Get user information

        :param pk: User ID
        :param username: Username
        :return:
        """
        async with async_db_session() as db:
            user = await user_dao.get_with_relation(db, user_id=pk, username=username)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            return user

    @staticmethod
    async def get_roles(*, pk: int) -> Sequence[Role]:
        """
        Get all roles of a user

        :param pk: User ID
        :return:
        """
        async with async_db_session() as db:
            user = await user_dao.get_with_relation(db, user_id=pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            return user.roles

    @staticmethod
    async def get_select(*, dept: int, username: str, phone: str, status: int) -> Select:
        """
        Get user list query conditions

        :param dept: Department ID
        :param username: Username
        :param phone: Phone number
        :param status: Status
        :return:
        """
        return await user_dao.get_list(dept=dept, username=username, phone=phone, status=status)

    @staticmethod
    async def create(*, request: Request, obj: AddUserParam) -> None:
        """
        Create user

        :param request: FastAPI request object
        :param obj: User creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            if await user_dao.get_by_username(db, obj.username):
                raise errors.ConflictError(msg='Username already registered')
            obj.nickname = obj.nickname if obj.nickname else f'#{random.randrange(88888, 99999)}'
            if not obj.password:
                raise errors.RequestError(msg='Password cannot be empty')
            if not await dept_dao.get(db, obj.dept_id):
                raise errors.NotFoundError(msg='Department does not exist')
            for role_id in obj.roles:
                if not await role_dao.get(db, role_id):
                    raise errors.NotFoundError(msg='Role does not exist')
            await user_dao.add(db, obj)

    @staticmethod
    async def update(*, request: Request, pk: int, obj: UpdateUserParam) -> int:
        """
        Update user information

        :param request: FastAPI request object
        :param pk: User ID
        :param obj: User update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get_with_relation(db, user_id=pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if request.user.username != user.username:
                raise errors.ForbiddenError(msg='Can only modify your own information')
            if obj.username != user.username:
                if await user_dao.get_by_username(db, obj.username):
                    raise errors.ConflictError(msg='Username already registered')
            for role_id in obj.roles:
                if not await role_dao.get(db, role_id):
                    raise errors.NotFoundError(msg='Role does not exist')
            count = await user_dao.update(db, user, obj)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_superuser(*, request: Request, pk: int) -> int:
        """
        Update user admin status

        :param request: FastAPI request object
        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='Cannot modify your own permissions')
            count = await user_dao.set_super(db, pk, not user.status)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_staff(*, request: Request, pk: int) -> int:
        """
        Update user staff status

        :param request: FastAPI request object
        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='Cannot modify your own permissions')
            count = await user_dao.set_staff(db, pk, not user.is_staff)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_status(*, request: Request, pk: int) -> int:
        """
        Update user status

        :param request: FastAPI request object
        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='Cannot modify your own permissions')
            count = await user_dao.set_status(db, pk, 0 if user.status == 1 else 1)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_multi_login(*, request: Request, pk: int) -> int:
        """
        Update user multi-login status

        :param request: FastAPI request object
        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            multi_login = user.is_multi_login if pk != user.id else request.user.is_multi_login
            new_multi_login = not multi_login
            count = await user_dao.set_multi_login(db, pk, new_multi_login)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            token = get_token(request)
            token_payload = jwt_decode(token)
            if pk == user.id:
                # When the system admin modifies themselves, all tokens except the current one become invalid
                if not new_multi_login:
                    key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{user.id}'
                    await redis_client.delete_prefix(key_prefix, exclude=f'{key_prefix}:{token_payload.session_uuid}')
            else:
                # When the system admin modifies others, all their tokens become invalid
                if not new_multi_login:
                    key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{user.id}'
                    await redis_client.delete_prefix(key_prefix)
            return count

    async def update_permission(self, *, request: Request, pk: int, type: UserPermissionType) -> int:
        """
        Update user permission

        :param request: FastAPI request object
        :param pk: User ID
        :param type: Permission type
        :return:
        """
        match type:
            case UserPermissionType.superuser:
                count = await self.update_superuser(request=request, pk=pk)
            case UserPermissionType.staff:
                count = await self.update_staff(request=request, pk=pk)
            case UserPermissionType.status:
                count = await self.update_status(request=request, pk=pk)
            case UserPermissionType.multi_login:
                count = await self.update_multi_login(request=request, pk=pk)
            case _:
                raise errors.RequestError(msg='Permission type does not exist')
        return count

    @staticmethod
    async def reset_pwd(*, pk: int, obj: ResetPasswordParam) -> int:
        """
        Reset user password

        :param pk: User ID
        :param obj: Password reset parameters
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if not password_verify(obj.old_password, user.password):
                raise errors.RequestError(msg='Old password is incorrect')
            if obj.new_password != obj.confirm_password:
                raise errors.RequestError(msg='Passwords do not match')
            new_pwd = get_hash_password(obj.new_password, user.salt)
            count = await user_dao.reset_password(db, user.id, new_pwd)
            key_prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{user.id}',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user.id}',
                f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}',
            ]
            for prefix in key_prefix:
                await redis_client.delete_prefix(prefix)
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        Delete user

        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            count = await user_dao.delete(db, user.id)
            key_prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{user.id}',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user.id}',
            ]
            for key in key_prefix:
                await redis_client.delete_prefix(key)
            return count


user_service: UserService = UserService()
