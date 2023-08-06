# This file is part of the Extra-P software (http://www.scalasca.org/software/extra-p)
#
# Copyright (c) 2020, Technical University of Darmstadt, Germany
#
# This software may be modified and distributed under the terms of a BSD-style license.
# See the LICENSE file in the base directory for details.

import warnings
import functools


def doublewrap(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return func(args[0])
        else:
            return lambda f: func(f, *args, **kwargs)

    return wrapper


@doublewrap
def deprecated(func, replacement="", message="{name} is deprecated."):
    """This is decorator marks functions as deprecated."""
    msg = message.format(name=func.__name__)
    if replacement != "":
        msg += " "
        msg += replacement

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(msg,
                      category=DeprecationWarning,
                      stacklevel=2)
        return func(*args, **kwargs)
    return wrapper


def _deprecated_code(replacement="", message="The code part at {name} is deprecated."):
    """This is decorator marks functions as deprecated."""
    import inspect
    curframe = inspect.stack()
    msg = message.format(name=str(curframe[1][0]))
    if replacement != "":
        msg += " "
        msg += replacement
    warnings.warn(msg,
                  category=DeprecationWarning,
                  stacklevel=2)


deprecated.code = _deprecated_code
