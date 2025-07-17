#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.schedules import schedule

from backend.app.task.utils.tzcrontab import TzAwareCrontab

LOCAL_BEAT_SCHEDULE = {
    'Test sync task': {
        'task': 'task_demo',
        'schedule': schedule(5),
    },
    'Test async task': {
        'task': 'task_demo_async',
        'schedule': TzAwareCrontab('1'),
    },
    'Clean operation logs': {
        'task': 'backend.app.task.tasks.db_log.tasks.delete_db_opera_log',
        'schedule': TzAwareCrontab('0', '0', day_of_week='6'),
    },
    'Clean login logs': {
        'task': 'backend.app.task.tasks.db_log.tasks.delete_db_login_log',
        'schedule': TzAwareCrontab('0', '0', day_of_month='15'),
    },
}
