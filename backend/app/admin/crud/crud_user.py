#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bcrypt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Dept, Role, User
from backend.app.admin.schema.user import (
    AddOAuth2UserParam,
    AddUserParam,
    UpdateUserParam,
)
from backend.common.security.jwt import get_hash_password
from backend.utils.timezone import timezone


class CRUDUser(CRUDPlus[User]):
    """User database operation class"""

    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        """
        Get user details

        :param db: Database session
        :param user_id: User ID
        :return:
        """
        return await self.select_model(db, user_id)

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """
        Get user by username

        :param db: Database session
        :param username: Username
        :return:
        """
        return await self.select_model_by_column(db, username=username)

    async def get_by_nickname(self, db: AsyncSession, nickname: str) -> User | None:
        """
        Get user by nickname

        :param db: Database session
        :param nickname: User nickname
        :return:
        """
        return await self.select_model_by_column(db, nickname=nickname)

    async def update_login_time(self, db: AsyncSession, username: str) -> int:
        """
        Update user's last login time

        :param db: Database session
        :param username: Username
        :return:
        """
        return await self.update_model_by_column(db, {'last_login_time': timezone.now()}, username=username)

    async def add(self, db: AsyncSession, obj: AddUserParam) -> None:
        """
        Add user

        :param db: Database session
        :param obj: Add user parameters
        :return:
        """
        salt = bcrypt.gensalt()
        obj.password = get_hash_password(obj.password, salt)
        dict_obj = obj.model_dump(exclude={'roles'})
        dict_obj.update({'salt': salt})
        new_user = self.model(**dict_obj)

        stmt = select(Role).where(Role.id.in_(obj.roles))
        roles = await db.execute(stmt)
        new_user.roles = roles.scalars().all()

        db.add(new_user)

    async def add_by_oauth2(self, db: AsyncSession, obj: AddOAuth2UserParam) -> None:
        """
        Add user via OAuth2

        :param db: Database session
        :param obj: Register user parameters
        :return:
        """
        salt = bcrypt.gensalt()
        obj.password = get_hash_password(obj.password, salt)
        dict_obj = obj.model_dump()
        dict_obj.update({'is_staff': True, 'salt': salt})
        new_user = self.model(**dict_obj)

        stmt = select(Role)
        role = await db.execute(stmt)
        new_user.roles = [role.scalars().first()]  # Bind the first role by default

        db.add(new_user)

    async def update(self, db: AsyncSession, input_user: User, obj: UpdateUserParam) -> int:
        """
        Update user information

        :param db: Database session
        :param input_user: User instance
        :param obj: Update user parameters
        :return:
        """
        role_ids = obj.roles
        del obj.roles
        count = await self.update_model(db, input_user.id, obj)

        stmt = select(Role).where(Role.id.in_(role_ids))
        roles = await db.execute(stmt)
        input_user.roles = roles.scalars().all()
        return count

    async def update_avatar(self, db: AsyncSession, user_id: int, avatar: str) -> int:
        """
        Update user avatar

        :param db: Database session
        :param user_id: User ID
        :param avatar: Avatar URL
        :return:
        """
        return await self.update_model(db, user_id, {'avatar': avatar})

    async def delete(self, db: AsyncSession, user_id: int) -> int:
        """
        Delete user

        :param db: Database session
        :param user_id: User ID
        :return:
        """
        return await self.delete_model(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> User | None:
        """
        Check if email is already bound

        :param db: Database session
        :param email: Email address
        :return:
        """
        return await self.select_model_by_column(db, email=email)

    async def reset_password(self, db: AsyncSession, pk: int, new_pwd: str) -> int:
        """
        Reset user password

        :param db: Database session
        :param pk: User ID
        :param new_pwd: New password (already encrypted)
        :return:
        """
        return await self.update_model(db, pk, {'password': new_pwd})

    async def get_list(self, dept: int | None, username: str | None, phone: str | None, status: int | None) -> Select:
        """
        Get user list

        :param dept: Department ID
        :param username: Username
        :param phone: Phone number
        :param status: User status
        :return:
        """
        filters = {}

        if dept:
            filters['dept_id'] = dept
        if username:
            filters['username__like'] = f'%{username}%'
        if phone:
            filters['phone_like'] = f'%{phone}%'
        if status is not None:
            filters['status'] = status

        return await self.select_order(
            'id',
            'desc',
            load_options=[
                selectinload(self.model.dept).options(noload(Dept.parent), noload(Dept.children), noload(Dept.users)),
                selectinload(self.model.roles).options(noload(Role.users), noload(Role.menus), noload(Role.scopes)),
            ],
            **filters,
        )

    async def set_super(self, db: AsyncSession, user_id: int, is_super: bool) -> int:
        """
        Set user super admin status

        :param db: Database session
        :param user_id: User ID
        :param is_super: Is super admin
        :return:
        """
        return await self.update_model(db, user_id, {'is_superuser': is_super})

    async def set_staff(self, db: AsyncSession, user_id: int, is_staff: bool) -> int:
        """
        Set user backend login status

        :param db: Database session
        :param user_id: User ID
        :param is_staff: Can login to backend
        :return:
        """
        return await self.update_model(db, user_id, {'is_staff': is_staff})

    async def set_status(self, db: AsyncSession, user_id: int, status: int) -> int:
        """
        Set user status

        :param db: Database session
        :param user_id: User ID
        :param status: Status
        :return:
        """
        return await self.update_model(db, user_id, {'status': status})

    async def set_multi_login(self, db: AsyncSession, user_id: int, multi_login: bool) -> int:
        """
        Set user multi-login status

        :param db: Database session
        :param user_id: User ID
        :param multi_login: Allow multi-login
        :return:
        """
        return await self.update_model(db, user_id, {'is_multi_login': multi_login})

    async def get_with_relation(
        self, db: AsyncSession, *, user_id: int | None = None, username: str | None = None
    ) -> User | None:
        """
        Get user with related information

        :param db: Database session
        :param user_id: User ID
        :param username: Username
        :return:
        """
        filters = {}

        if user_id:
            filters['id'] = user_id
        if username:
            filters['username'] = username

        return await self.select_model_by_column(
            db,
            load_options=[selectinload(self.model.roles).options(selectinload(Role.menus), selectinload(Role.scopes))],
            load_strategies=['dept'],
            **filters,
        )


user_dao: CRUDUser = CRUDUser(User)
