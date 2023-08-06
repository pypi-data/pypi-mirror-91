# -*- coding: utf-8 -*-
# Author: Ztj
# Intro: Celery 应用
# Reference: https://fastapi.tiangolo.com/

from typing import Optional

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from ZtjCeleryApp import celery

api = FastAPI()


@api.get('/health', response_class=PlainTextResponse)
def health():
    """健康检查"""
    return 'ok'


@api.get('/tasks')
def tasks():
    """任务列表"""
    return celery.control.inspect().registered()


@api.post('/call')
def call(name, body: Optional[dict] = None):
    """任务调用"""
    body = dict() if body is None else body
    return celery.send_task(name, **body).get()
