#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.backends.database.session import SessionManager as CelerySessionManager


class SessionManager(CelerySessionManager):
    """
    Override celery SessionManager
    """

    def __init__(self):
        super().__init__()

        # Disable automatic creation of celery's internally defined task result tables
        self.prepared = True
