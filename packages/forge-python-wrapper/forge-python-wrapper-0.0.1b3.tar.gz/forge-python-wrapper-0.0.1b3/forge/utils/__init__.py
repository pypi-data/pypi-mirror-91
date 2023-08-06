# -*- coding: utf-8 -*-

"""documentation placeholder"""

from __future__ import absolute_import

import sys

from collections import deque
from json import dumps
from pprint import pformat

try:
    from collections.abc import Iterable, Mapping
except ImportError:
    from collections import Iterable, Mapping

from .logger import Logger  # noqa

if sys.version_info >= (3, 7):
    from .semaphore import HTTPSemaphore  # noqa: F401


def pretty_print(obj, sort=True, _print=True):
    """ """
    try:
        if isinstance(obj, Mapping):
            output = _pretty_print(_clean(obj, sort))
        elif isinstance(obj, Iterable):
            output = _pretty_print(_clean(obj, False))
        else:
            output = _pretty_print(_obj_to_dict(obj), sort)
    except TypeError:
        output = pformat(obj, indent=4, width=3)

    if _print:
        print(output)
    return output


def _pretty_print(obj, sort=True):
    return dumps(obj, sort_keys=sort, indent=4, ensure_ascii=False)


def _obj_to_dict(obj):
    try:
        d = {pformat(obj): _clean(obj.__dict__)}
    except AttributeError:
        d = {pformat(obj): None}
    return d


def _clean(obj, is_mapping=True):
    if is_mapping:
        clean_data = {}
        iterable = obj.items()
    else:
        clean_data = []
        iterable = obj

    for item in iterable:
        if is_mapping:
            k, v = item
        else:
            v = item

        if isinstance(v, str):
            v = v
        elif isinstance(v, deque):
            v = _clean(list(v))
        elif isinstance(v, Mapping):
            v = _clean(v)
        elif isinstance(v, Iterable):
            v = _clean(v, False)
        elif type(v) not in (int, float, dict, list, bool, type(None)):
            v = _obj_to_dict(v)

        if is_mapping:
            clean_data[str(k)] = v
        else:
            clean_data.append(v)

    return clean_data
