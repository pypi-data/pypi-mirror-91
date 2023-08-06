# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from functools import wraps
from contextlib import contextmanager


_warned = set()
_warning_silenced_for = None


def deprecated(target, replacement=None):
    def monitor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global _warning_silenced_for
            if _warning_silenced_for is None:
                _warn_deprecation(target, replacement)  # only raise warning for top-level invocation
                _warning_silenced_for = target
            result = func(*args, **kwargs)
            if _warning_silenced_for == target:
                _warning_silenced_for = None
            return result
        return wrapper
    return monitor


@contextmanager
def silent_deprecation_warning():
    global _warning_silenced_for
    _warning_silenced_for = '__WARNING_DISABLED__'
    try:
        yield
    finally:
        _warning_silenced_for = None


def _warn_deprecation(target, replacement=None):
    global _warned
    if target in _warned:
        return  # only warn per target per session
    msg = '{} is deprecated after version 1.0.69.'.format(target)
    if replacement:
        msg += ' Please use {}.'.format(replacement)
    msg += ' See Dataset API change notice at https://aka.ms/dataset-deprecation.'
    logging.getLogger().warning(msg)
    _warned.add(target)
