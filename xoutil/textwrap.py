# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.textwrap
#----------------------------------------------------------------------
# Copyright (c) 2014 Merchise Autrement and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 2014-02-26

'''Text wrapping and filling.

Exposes all original `string` module functionalities, with some general
additions.

In this module `str` and `unicode` types are not used because Python 2.x and
Python 3.x treats strings differently, `bytes` and `_unicode` will be used
instead with the following conventions:

- In Python 2.x `str` is synonym of `bytes` and both (`unicode` and 'str') are
  both string types inheriting form `basestring`.  `_unicode` is synonym of
  `unicode`.

- In Python 3.x `str` is always unicode but `unicode` and `basestring` types
  doesn't exists. `bytes` type can be used as an array of one byte each item.

  `_unicode` is synonym of `str`.

  Many methods are readjusted to these conditions.

'''

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_abs_import)

from xoutil.modules import copy_members as _copy_python_module_members
_pm = _copy_python_module_members()
_pm_dedent = _pm.dedent
_pm_indent = getattr(_pm, 'indent', None)

del _pm, _copy_python_module_members


def dedent(text, skip_firstline=False):
    '''Remove any common leading whitespace from every line in text.

    This can be used to make triple-quoted strings line up with the left edge
    of the display, while still presenting them in the source code in indented
    form.

    Note that tabs and spaces are both treated as whitespace, but they are not
    equal: the lines "\ \ \ \ hello" and "\\thello" are considered to have no
    common leading whitespace.

    If `skip_firstline` is True, the first line is separated from the rest of
    the body.  This helps with docstrings that follow :pep:`257`.
    '''
    if skip_firstline:
        parts = text.split('\n', 1)
        if len(parts) > 1:
            subject, body = parts
        else:
            subject, body = parts[0], ''
        result = _pm_dedent(subject)
        if body:
            result += '\n' + _pm_dedent(body)
    else:
        result = _pm_dedent(text)
    return result


if not _pm_indent:
    def indent(text, prefix, predicate=None):
        """Adds 'prefix' to the beginning of selected lines in 'text'.

        If 'predicate' is provided, 'prefix' will only be added to the lines
        where 'predicate(line)' is True. If 'predicate' is not provided, it
        will default to adding 'prefix' to all non-empty lines that do not
        consist solely of whitespace characters.

        """
        if predicate is None:
            def predicate(line):
                return line.strip()

        def prefixed_lines():
            for line in text.splitlines(True):
                yield (prefix + line if predicate(line) else line)
        return ''.join(prefixed_lines())