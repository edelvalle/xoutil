#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.deprecation
#----------------------------------------------------------------------
# Copyright (c) 2012, 2013 Merchise Autrement and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on Feb 15, 2012

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_abs_imports)

import types
import warnings

from functools import wraps
from xoutil.compat import class_types as _class_types

__docstring_format__ = 'rst'
__author__ = 'manu'


DEFAULT_MSG = ('{funcname} is now deprecated and it will be removed{in_version}. ' +
              'Use {replacement} instead.')


class DeprecationError(Exception):
    pass


# XXX: Don't make deprecated depends upon anything more than compat and
# decorator.py. Since this is meant to be used by all others xoutil modules.
def deprecated(replacement, msg=DEFAULT_MSG, deprecated_module=None, removed_in_version=None, check_version=False):
    '''Small decorator for deprecated functions.

    Usage::

        @deprecate(new_function)
        def deprecated_function(...):
            ...
    '''
    def decorator(target):
        def raise_if_deprecated(target_version):
            import pkg_resources
            from xoutil.compat import str_base
            from xoutil.names import nameof
            xoutil_dist = pkg_resources.get_distribution('xoutil')
            if isinstance(target_version, str_base):
                target_version = pkg_resources.parse_version(target_version)
            if xoutil_dist.parsed_version >= target_version:
                msg = ('A deprecated feature %r was scheduled to be '
                       'removed in version %r and it is still '
                       'alive in %r!' % (nameof(target, inner=True, full=True),
                                         str(removed_in_version),
                                         str(xoutil_dist.version)))
                raise DeprecationError(msg)

        if deprecated_module:
            funcname = deprecated_module + '.' + target.__name__
        else:
            funcname = target.__name__
        if isinstance(replacement, _class_types + (types.FunctionType, )):
            repl_name = replacement.__module__ + '.' + replacement.__name__
        else:
            repl_name = replacement
        if removed_in_version:
            in_version = ' in version ' + removed_in_version
        else:
            in_version = ''
        if isinstance(target, _class_types):
            def new(*args, **kwargs):
                if check_version and removed_in_version:
                    raise_if_deprecated(removed_in_version)
                warnings.warn(msg.format(funcname=funcname,
                                         replacement=repl_name,
                                         in_version=in_version),
                              stacklevel=2)
                return target.__new__(*args, **kwargs)
            # Code copied and adapted from xoutil.objects.copy_class. This is
            # done so because this module *must* not depends on any other,
            # otherwise an import cycle might be formed when deprecating a
            # class in xoutil.objects.
            from xoutil.compat import iteritems_
            from xoutil.types import MemberDescriptorType
            meta = type(target)
            attrs = {name: value
                     for name, value in iteritems_(target.__dict__)
                     if name not in ('__class__', '__mro__', '__name__', '__weakref__', '__dict__')
                     # Must remove member descriptors, otherwise the old's class
                     # descriptor will override those that must be created here.
                     if not isinstance(value, MemberDescriptorType)}
            attrs.update(__new__=new)
            result = meta(target.__name__, target.__bases__, attrs)
            return result
        else:
            @wraps(target)
            def inner(*args, **kw):
                if check_version and removed_in_version:
                    raise_if_deprecated(removed_in_version)
                warnings.warn(msg.format(funcname=funcname,
                                         replacement=repl_name,
                                         in_version=in_version),
                              stacklevel=2)
                return target(*args, **kw)
            return inner
    return decorator


def inject_deprecated(funcnames, source, target=None):
    '''
    Takes a sequence of function names `funcnames` which reside in the `source`
    module and injects them into `target` marked as deprecated. If `target` is
    None then we inject the functions into the locals of the calling code. It's
    expected it's a module.

    This function is provided for easing the deprecation of whole modules and
    should not be used to do otherwise.
    '''
    if not target:
        import sys
        frame = sys._getframe(1)
        try:
            target_locals = frame.f_locals
        finally:
            # As recommended to avoid memory leaks
            del frame
    else:
        pass
    for targetname in funcnames:
        unset = object()
        target = getattr(source, targetname, unset)
        if target is not unset:
            if isinstance(target, (types.FunctionType, types.LambdaType) + _class_types):
                replacement = source.__name__ + '.' + targetname
                module_name = target_locals.get('__name__', None)
                target_locals[targetname] = deprecated(replacement,
                                                       DEFAULT_MSG,
                                                       module_name)(target)
            else:
                target_locals[targetname] = target
        else:
            warnings.warn('{targetname} was expected to be in {source}'.
                          format(targetname=targetname,
                                 source=source.__name__), stacklevel=2)
