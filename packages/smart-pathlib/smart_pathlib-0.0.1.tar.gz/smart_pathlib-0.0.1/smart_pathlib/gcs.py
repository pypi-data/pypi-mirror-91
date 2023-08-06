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

from google.cloud import storage

import smart_pathlib.util

SCHEME = 'gs'


def parse_uri(uri_as_string):
    sr = smart_pathlib.util.safe_urlsplit(uri_as_string)
    assert sr.scheme == SCHEME
    bucket_id = sr.netloc
    blob_id = sr.path.lstrip('/')
    return dict(scheme=SCHEME, bucket_id=bucket_id, blob_id=blob_id)


def exists(uri, transport_params):
    parsed_uri = parse_uri(uri)
    kwargs = smart_pathlib.util.check_kwargs(_exists, transport_params)
    return _exists(parsed_uri['bucket_id'], parsed_uri['blob_id'], **kwargs)


def stat(uri, transport_params):
    parsed_uri = parse_uri(uri)
    kwargs = smart_pathlib.util.check_kwargs(_stat, transport_params)
    return _stat(parsed_uri['bucket_id'], parsed_uri['blob_id'], **kwargs)


def _exists(bucket_id, blob_id, client=None):
    if client is None:
        client = storage.Client()
    bucket = client.bucket(bucket_id)
    blob = bucket.blob(blob_id)
    return blob.exists()


def _stat(bucket_id, blob_id, client=None):
    if client is None:
        client = storage.Client()
    bucket = client.bucket(bucket_id)
    blob = bucket.get_blob(blob_id)
    stat_result = os.stat_result((
        -1,  # st_mode
        -1,  # st_ino
        -1,  # st_dev
        -1,  # st_nlink
        -1,  # st_uid
        -1,  # st_gid
        blob.size,  # st_size
        -1,  # st_atime
        -1,  # st_mtime
        -1,  # st_ctime
    ))
    return stat_result
