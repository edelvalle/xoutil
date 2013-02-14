#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.decorator.compat
#----------------------------------------------------------------------
# Copyright (c) 2013 Merchise Autrement and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under
# the terms of the LICENCE attached in the distribution package.
#
# Created on 2013-01-15

'''Provides decorators related with interoperability Python 2 and Python 3.

'''

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_abs_imports)

__author__ = "Manuel Vázquez Acosta <mva.led@gmail.com>"
__date__   = "Tue Jan 15 11:38:55 2013"


def metaclass(meta):
    '''Declares a meta class transparently in Python 2 and Python 3.

    Example::

        >>> class Metaclass(type):
        ...     pass

        >>> @metaclass(Metaclass)
        ... class Something(object):
        ...    pass

        >>> type(Something)    # doctest: +ELLIPSIS
        <class '...Metaclass'>

    '''
    def decorator(cls):
        from xoutil.compat import iteritems_
        attrs = {name: value for name, value in iteritems_(cls.__dict__) if
                 name not in ('__class__', '__mro__', '__name__', '__doc__',
                              '__weakref__')}
        result = meta(cls.__name__, cls.__bases__, attrs)
        result.__doc__ = cls.__doc__
        return result
    return decorator