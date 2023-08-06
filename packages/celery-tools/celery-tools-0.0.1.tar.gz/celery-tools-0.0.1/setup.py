# -*- coding: utf-8 -*-
# Intro: Celery 工具模块
# Author: Ztj
# Email: ztj1993@gmail.com

import os.path

from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf8')
readme = f.read()
f.close()

setup(
    name='celery-tools',
    version='0.0.1',
    description='celery tools',
    long_description=readme,
    long_description_content_type='text/markdown',
    py_modules=['ZtjCeleryApp', 'ZtjCeleryApi'],
    url='https://github.com/ztj1993/py-celery-tools',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',
    keywords='fastapi celery',
    license='MIT License',
    install_requires=[
        'fastapi',
        'celery',
    ],
)
