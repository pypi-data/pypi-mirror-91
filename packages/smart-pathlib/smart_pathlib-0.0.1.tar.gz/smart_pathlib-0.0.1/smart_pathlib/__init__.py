# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Guillaume Fournier <fournierg@gmail.com>
#
# This file is forked from `smart_open` project.
#
# This code is distributed under the terms and conditions
# from the MIT License (MIT).
#

from smart_pathlib import version
from .library import exists, stat

__all__ = ["exists", "stat"]

__version__ = version.__version__
