#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.oauth2.model import UserSocial
from backend.plugin.oauth2.schema.user_social import CreateUserSocialParam


class CRUDUserSocial(CRUDPlus[UserSocial]):
    """Database operations class for user social accounts"""

    async def check_binding(self, db: AsyncSession, pk: int, source: str) -> UserSocial | None:
        """
        Check if a system user has a social account binding

        :param db: Database session
        :param pk: User ID
        :param source: Social account type
        :return:
        """
        return await self.select_model_by_column(db, user_id=pk, source=source)

    async def get_by_sid(self, db: AsyncSession, sid: str, source: str) -> UserSocial | None:
        """
        Get social user by UUID

        :param db: Database session
        :param sid: Third-party UUID
        :param source: Social account type
        :return:
        """
        return await self.select_model_by_column(db, sid=sid, source=source)

    async def create(self, db: AsyncSession, obj: CreateUserSocialParam) -> None:
        """
        Create a user social account binding

        :param db: Database session
        :param obj: Parameters for creating user social account binding
        :return:
        """
        await self.create_model(db, obj)

    async def delete(self, db: AsyncSession, social_id: int) -> int:
        """
        Delete a user social account binding

        :param db: Database session
        :param social_id: Social account binding ID
        :return:
        """
        return await self.delete_model(db, social_id)


user_social_dao: CRUDUserSocial = CRUDUserSocial(UserSocial)
