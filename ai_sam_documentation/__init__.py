# -*- coding: utf-8 -*-
from . import controllers
from .scripts.build_courses import build_courses


def post_init_hook(env):
    """Build courses from docs/ folder after install/upgrade."""
    build_courses(env)
