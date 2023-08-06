# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Guillaume Fournier <fournierg@gmail.com>
#
# This file is forked from `smart_open` project.
#
# This code is distributed under the terms and conditions
# from the MIT License (MIT).
#

"""Main API for smart_pathlib.

Main functions are:
- exists()
- stat()
"""
import os
import pathlib
import urllib.parse

from smart_pathlib import transport


def _sniff_scheme(uri_as_string):
    """Returns the scheme of the URL only, as a string."""
    #
    # urlsplit doesn't work on Windows -- it parses the drive as the scheme...
    # no protocol given => assume a local file
    #
    if os.name == 'nt' and '://' not in uri_as_string:
        uri_as_string = 'file://' + uri_as_string

    return urllib.parse.urlsplit(uri_as_string).scheme


def _check_uri(uri):
    """Checks if the URI is valid and returns the string form of the URI."""
    if isinstance(uri, pathlib.Path):
        uri = str(uri)

    assert isinstance(uri, str),\
        "URI must be a 'str' or a 'pathlib.Path' instance"

    return uri


def exists(uri, transport_params=None):
    """Return `True` if `uri` refers to an existing path, `False` otherwise.

    Parameters
    ----------
    uri: str or path object
        The URI to test for existence
    transport_params: dict, optional
        Additional parameters for the transport layer

    Returns
    -------
    `True` if object exists, `False` otherwise

    See Also
    --------
    - https://docs.python.org/3/library/os.path.html#os.path.exists
    """
    if transport_params is None:
        transport_params = {}
    uri = _check_uri(uri)
    scheme = _sniff_scheme(uri)
    submodule = transport.get_transport(scheme)
    return submodule.exists(uri, transport_params)


def stat(uri, transport_params=None):
    """Return the status of a file URI

    Parameters
    ----------
    uri: str or path object
        The URI of object
    transport_params: dict, optional
        Additional parameters for the transport layer

    Returns
    -------
    a `os.stat_result` instance

    See Also
    --------
    - https://docs.python.org/3/library/os.html#os.stat
    """
    if transport_params is None:
        transport_params = {}
    uri = _check_uri(uri)
    scheme = _sniff_scheme(uri)
    submodule = transport.get_transport(scheme)
    return submodule.stat(uri, transport_params)
