## Task Introduction

The current tasks are implemented using Celery. For implementation details, please refer to [#225](https://github.com/fastapi-practices/fastapi_best_architecture/discussions/225).

## Scheduled Tasks

Write related scheduled tasks in the `backend/app/task/tasks/beat.py` file.

### Simple Tasks

Write related task code in the `backend/app/task/tasks/tasks.py` file.

### Hierarchical Tasks

If you want to organize tasks into directories for a clearer structure, you can create any directory you like, but please note:

1. Create a new Python package directory under `backend/app/task/tasks`.
2. After creating the directory, be sure to update the `CELERY_TASKS_PACKAGES` list in the `conf.py` configuration file to include the new module path.
3. In the new directory, be sure to add a `tasks.py` file and write the related task code in it.

## Message Broker

You can control the message broker selection via `CELERY_BROKER`. It supports both Redis and RabbitMQ.

For local debugging, it is recommended to use Redis.

For production environments, RabbitMQ is required.
