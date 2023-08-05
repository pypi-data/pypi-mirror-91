# -*- coding: utf-8 -*-
'''
environments module for reinforcement learning
==============================================

This module contains classes that provides tools to load/save objects and
environments, add/remove `agents`/`subjects`, assign `agents` to `subjects` and
run models.

Classes
-------
Environment:
    The base class of all environment classes.

EnvironmentStaticMap:
    An environment with static interaction map.
'''

from .environment import Environment  # noqa: W0611
from .environment_static_map import EnvironmentStaticMap  # noqa: W0611
