#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import uvicorn

if __name__ == '__main__':
    # Why have a separate startup file: https://stackoverflow.com/questions/64003384

    # DEBUG:
    # If you prefer to debug in your IDE, you can directly right-click and run this file in the IDE.
    # If you prefer to debug using print statements, it is recommended to start the service using the fba cli.

    # Warning:
    # If you are starting this file using the python command, please follow these instructions:
    # 1. Install dependencies using uv as per the official documentation.
    # 2. Make sure your command line working directory is the backend directory.
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
