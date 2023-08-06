# -*- coding: utf-8 -*-
# Author: Ztj
# Intro: Celery 应用
# Reference: https://docs.celeryproject.org/en/stable/userguide/application.html

import os

from celery import Celery

name = os.environ.get('CELERY_APP', 'celery')

setting = dict(
    result_backend='rpc',
    result_persistent=False,
    timezone=os.environ.get('CELERY_TIMEZONE', 'Asia/Shanghai'),
    result_expires=os.environ.get('CELERY_RESULT_EXPIRES', 3600),
)

celery = Celery(name)
celery.config_from_object(setting)
