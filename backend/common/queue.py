#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from asyncio import Queue


async def batch_dequeue(queue: Queue, max_items: int, timeout: float) -> list:
    """
    Get multiple items from an async queue.

    :param queue: The `asyncio.Queue` to get items from
    :param max_items: Maximum number of items to retrieve from the queue
    :param timeout: Total wait timeout in seconds
    :return:
    """
    items = []

    async def collector():
        while len(items) < max_items:
            item = await queue.get()
            items.append(item)

    try:
        await asyncio.wait_for(collector(), timeout=timeout)
    except asyncio.TimeoutError:
        pass

    return items
