#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.enums import IntEnum, StrEnum


class TaskSchedulerType(IntEnum):
    """Task scheduling type"""

    INTERVAL = 0
    CRONTAB = 1


class PeriodType(StrEnum):
    """Period type"""

    DAYS = 'days'
    HOURS = 'hours'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    MICROSECONDS = 'microseconds'
