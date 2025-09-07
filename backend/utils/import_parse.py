#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib
import inspect

from functools import lru_cache
from typing import Any, Type, TypeVar

from backend.common.exception import errors
from backend.common.log import log

T = TypeVar('T')


@lru_cache(maxsize=512)
def import_module_cached(module_path: str) -> Any:
    """
    Cached import of a module

    :param module_path: Module path
    :return:
    """
    return importlib.import_module(module_path)


def dynamic_import_data_model(module_path: str) -> Type[T]:
    """
    Dynamically import a data model

    :param module_path: Module path in the format 'module_path.class_name'
    :return:
    """
    try:
        module_path, class_name = module_path.rsplit('.', 1)
        module = import_module_cached(module_path)
        return getattr(module, class_name)
    except Exception as e:
        log.error(f'Failed to dynamically import data model: {e}')
        raise errors.ServerError(msg='Failed to dynamically parse data model columns, please contact the system super administrator')


def get_model_object(module_path: str) -> type | None:
    """
    Get model object

    :param module_path: Module path
    :return:
    """
    try:
        module = import_module_cached(module_path)
    except ModuleNotFoundError:
        log.warning(f'Module {module_path} does not contain a model object')
        return None
    except Exception as e:
        raise RuntimeError(f'Failed to get model object from module {module_path}: {e}')

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            return obj

    return None
