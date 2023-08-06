# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Guillaume Fournier <fournierg@gmail.com>
#
# This file is forked from `smart_open` project.
#
# This code is distributed under the terms and conditions
# from the MIT License (MIT).
#
import os


SCHEME = 'file'


def exists(uri, transport_params):
    return os.path.exists(uri)


def stat(uri, transport_params):
    return os.stat(uri)
