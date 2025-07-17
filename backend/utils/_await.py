#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import atexit
import threading
import weakref

from typing import Awaitable, Callable, TypeVar

T = TypeVar('T')


class _TaskRunner:
    """A task runner that runs an asyncio event loop on a background thread."""

    def __init__(self):
        self.__loop: asyncio.AbstractEventLoop | None = None
        self.__thread: threading.Thread | None = None
        self.__lock = threading.Lock()
        atexit.register(self.close)

    def close(self):
        """Close the event loop"""
        if self.__loop:
            self.__loop.stop()

    def _target(self):
        """Background thread target"""
        loop = self.__loop
        try:
            loop.run_forever()
        finally:
            loop.close()

    def run(self, coro):
        """Synchronously run a coroutine on the background thread"""
        with self.__lock:
            name = f'{threading.current_thread().name} - runner'
            if self.__loop is None:
                self.__loop = asyncio.new_event_loop()
                self.__thread = threading.Thread(target=self._target, daemon=True, name=name)
                self.__thread.start()
        fut = asyncio.run_coroutine_threadsafe(coro, self.__loop)
        return fut.result(None)


_runner_map = weakref.WeakValueDictionary()


def run_await(coro: Callable[..., Awaitable[T]]) -> Callable[..., T]:
    """Wrap a coroutine in a function that blocks until it finishes"""

    def wrapped(*args, **kwargs):
        name = threading.current_thread().name
        inner = coro(*args, **kwargs)
        try:
            # If an event loop is running in this thread,
            # use the task runner
            asyncio.get_running_loop()
            if name not in _runner_map:
                _runner_map[name] = _TaskRunner()
            return _runner_map[name].run(inner)
        except RuntimeError:
            # If not, create a new event loop
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(inner)

    wrapped.__doc__ = coro.__doc__
    return wrapped
