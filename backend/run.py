#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import uvicorn

if __name__ == '__main__':
    # Why use a separate startup file: https://stackoverflow.com/questions/64003384
    # If you prefer debugging in an IDE, you can directly right-click and run this file in the IDE
    # If you prefer debugging with print statements, it is recommended to start the service using the FastAPI CLI
    try:
        uvicorn.run(
            app='backend.main:app',
            host='127.0.0.1',
            port=8000,
            reload=True,
            reload_excludes=[os.path.abspath('../.venv')],
        )
    except Exception as e:
        raise e
