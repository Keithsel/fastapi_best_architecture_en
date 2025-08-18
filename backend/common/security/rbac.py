#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Depends, Request

from backend.common.enums import MethodType, StatusType
from backend.common.exception import errors
from backend.common.log import log
from backend.common.security.jwt import DependsJwtAuth
from backend.core.conf import settings
from backend.utils.import_parse import import_module_cached


async def rbac_verify(request: Request, _token: str = DependsJwtAuth) -> None:
    """
    RBAC permission verification (the order of authentication is important, modify with caution)

    :param request: FastAPI request object
    :param _token: JWT token
    :return:
    """
    path = request.url.path

    # API authentication whitelist
    if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
        return
    for pattern in settings.TOKEN_REQUEST_PATH_EXCLUDE_PATTERN:
        if pattern.match(path):
            return

    # Force JWT authorization status check
    if not request.auth.scopes:
        raise errors.TokenError

    # Super administrator exemption from verification
    if request.user.is_superuser:
        return

    # Check user roles
    user_roles = request.user.roles
    if not user_roles or all(status == 0 for status in user_roles):
        raise errors.AuthorizationError(msg='User has not been assigned a role, please contact the system administrator')

    # Check user role menus
    if not any(len(role.menus) > 0 for role in user_roles):
        raise errors.AuthorizationError(msg='User has not been assigned a menu, please contact the system administrator')

    # Check backend management operation permissions
    method = request.method
    if method != MethodType.GET or method != MethodType.OPTIONS:
        if not request.user.is_staff:
            raise errors.AuthorizationError(msg='User is prohibited from backend management operations, please contact the system administrator')

    # RBAC authentication
    if settings.RBAC_ROLE_MENU_MODE:
        path_auth_perm = getattr(request.state, 'permission', None)

        # No menu operation permission identifier, do not verify
        if not path_auth_perm:
            return

        # Menu authentication whitelist
        if path_auth_perm in settings.RBAC_ROLE_MENU_EXCLUDE:
            return

        # Deduplicate menus
        unique_menus = {}
        for role in user_roles:
            for menu in role.menus:
                unique_menus[menu.id] = menu

        # Check assigned menu permissions
        allow_perms = []
        for menu in list(unique_menus.values()):
            if menu.perms and menu.status == StatusType.enable:
                allow_perms.extend(menu.perms.split(','))
        if path_auth_perm not in allow_perms:
            raise errors.AuthorizationError
    else:
        try:
            casbin_rbac = import_module_cached('backend.plugin.casbin_rbac.rbac')
            casbin_verify = getattr(casbin_rbac, 'casbin_verify')
        except (ImportError, AttributeError) as e:
            log.error(f'RBAC permission verification is being performed via casbin, but this plugin does not exist: {e}')
            raise errors.ServerError(msg='Permission verification failed, please contact the system administrator')

        await casbin_verify(request)


# RBAC authorization dependency injection
DependsRBAC = Depends(rbac_verify)
