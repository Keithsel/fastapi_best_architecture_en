#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from backend.common.log import log
from backend.core.conf import settings


class RedisCli(Redis):
    """Redis Client"""

    def __init__(self) -> None:
        """Initialize Redis Client"""
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            socket_connect_timeout=settings.REDIS_TIMEOUT,
            socket_keepalive=True,  # Keep connection alive
            health_check_interval=30,  # Health check interval
            decode_responses=True,  # Decode as utf-8
        )

    async def open(self) -> None:
        """Trigger initial connection"""
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ Redis database connection timed out')
            sys.exit()
        except AuthenticationError:
            log.error('❌ Redis database authentication failed')
            sys.exit()
        except Exception as e:
            log.error('❌ Redis database connection error {}', e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None) -> None:
        """
        Delete all keys with the specified prefix

        :param prefix: Prefix
        :param exclude: Keys to exclude
        :return:
        """
        keys = []
        async for key in self.scan_iter(match=f'{prefix}*'):
            if isinstance(exclude, str):
                if key != exclude:
                    keys.append(key)
            elif isinstance(exclude, list):
                if key not in exclude:
                    keys.append(key)
            else:
                keys.append(key)
        if keys:
            await self.delete(*keys)


# Create Redis client singleton
redis_client: RedisCli = RedisCli()
