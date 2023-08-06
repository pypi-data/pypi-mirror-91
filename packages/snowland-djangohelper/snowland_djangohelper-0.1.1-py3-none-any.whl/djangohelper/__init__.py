#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: __init__.py
# @time: 2018/7/23 14:46
# @Software: PyCharm

from djangohelper.project2lines import project_to_lines
from djangohelper.util import create_admin, createView, trans
from djangohelper.viewhelper import generate_paginator_result
from djangohelper.requests import request
from djangohelper.common import *
from django.utils.version import get_version
from djangohelper.viewsets import *
from djangohelper.responses import *
from djangohelper.permissions import *

VERSION = (0, 1, 1, 'final', 0)

__version__ = get_version(VERSION)

def setup(set_prefix=True):
    """
    Configure the settings (this happens as a side effect of accessing the
    first setting), configure logging and populate the app registry.
    Set the thread-local urlresolvers script prefix if `set_prefix` is True.
    """
    from djangohelper.apps import apps
    from djangohelper.conf import settings
    from django.urls import set_script_prefix
    from django.utils.log import configure_logging

    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    if set_prefix:
        set_script_prefix(
            '/' if settings.FORCE_SCRIPT_NAME is None else settings.FORCE_SCRIPT_NAME
        )
    apps.populate(settings.INSTALLED_APPS)
