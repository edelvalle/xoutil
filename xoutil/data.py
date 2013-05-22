# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.data
#----------------------------------------------------------------------
# Copyright (c) 2013 Merchise Autrement and Contributors
# Copyright (c) 2009-2012 Medardo Rodríguez
# All rights reserved.
#
# Author: Medardo Rodriguez
# Contributors: see CONTRIBUTORS and HISTORY file
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.

'''Some useful Data Structures and data-related algorithms and functions.

.. warning::

   **This module is completely deprecated since 1.4.0**. Most of its contents
   are already deprecated.

'''


from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_absimports)

import xoutil.collections
from xoutil.deprecation import deprecated

@deprecated('xoutil.objects.smart_copy')
def smart_copy(source, target, full=False):
    '''Copies attributes (or keys) from `source` to `target`.

    .. warning::

       *Deprecated since 1.4.0*. Use :func:`xoutil.objects.smart_copy`. Using
       the new function this one is roughly equivalent to::

           from xoutil.objects import smart_copy
           smart_copy(source, target, defaults=full)

    '''
    from xoutil.objects import smart_copy as _smart_copy
    return _smart_copy(source, target, defaults=full)

def adapt_exception(value, **kwargs):
    '''Like PEP-246, Object Adaptation, with ``adapt(value, Exception,
    None)``.

    If the value is not an exception is expected to be a tuple/list which
    contains an Exception type as its first item.

    '''
    isi, issc, ebc = isinstance, issubclass, Exception
    if isi(value, ebc) or isi(value, type) and issc(value, ebc):
        return value
    elif isi(value, (tuple, list)) and len(value) > 0 and issc(value[0], ebc):
        from xoutil.compat import str_base
        iss = lambda s: isinstance(s, str_base)
        ecls = value[0]
        args = ((x.format(**kwargs) if iss(x) else x) for x in value[1:])
        return ecls(*args)
    else:
        return None


@deprecated(xoutil.collections.SmartDict)
class SmartDict(xoutil.collections.SmartDict):
    '''A smart dict that extends the `update` method to accept several args.

    .. warning::

       Deprecated since 1.4.0. Moved to
       :class:`xoutil.collections.SmartDict`.

    '''

@deprecated(xoutil.collections.OrderedSmartDict)
class SortedSmartDict(xoutil.collections.OrderedSmartDict):
    '''An ordered SmartDict.

    .. warning::

       Deprecated since 1.4.0. Moved to
       :class:`xoutil.collections.OrderedSmartDict`.

    '''

class IntSet(object):
    '''Compacted non-negative integer set with smart representation.
    '''
    def __init__(self, init=None):
        # TODO: Create sparce mutable bytes slices
        self._bucket_size = 4096
        self._count = 0
        self._content = []   # each byte represents 1024 members (ie. 512 bytes)
        if init:
            self._extend(init)

    def __contains__(self, item):
        from xoutil.compat import integers
        assert isinstance(item, integers) and item >= 0
        b = self._content
        if not b:
            return False
        index, bit = divmod(item, self._bucket_size)
        size = len(b)
        if size > index:
            bucket = b[index]
            return (2**bit) & bucket == 2**bit
        else:
            return False

    def add(self, item):
        '''Adds an item to the set.
        '''
        b = self._content
        index, bit = divmod(item, self._bucket_size)
        size = len(b)
        if size <= index:
            from itertools import repeat
            pad = index - size + 1
            b.extend(repeat(0, pad))
        bucket = b[index]
        bucket = bucket | 2**bit
        b[index] = bucket
        self._count += 1

    def remove(self, item):
        '''Removes an item to the set.
        '''
        b = self._content
        index, bit = divmod(item, self._bucket_size)
        size = len(b)
        if size <= index:
            return
        bucket = b[index]
        bucket = bucket & ~2**bit
        b[index] = bucket
        self._count -= 1
        if index == size - 1:
            # compact
            while b and b[-1] == 0:
                b.pop(-1)

    def __repr__(self):
        b = self._content
        if not b:
            return b'<empty intset>'
        subsets = []
        index = 0
        size = len(b)
        while index < size:
            while index < size and b[index] == 0:
                index += 1
            if index < size:
                bucket, bit = b[index], 0
                while bucket & (2**bit) == 0:
                    bit += 1
                first = index * self._bucket_size + bit
                sset = (first, first)
                while bit < self._bucket_size:
                    bit += 1
                    while bit < self._bucket_size and bucket & (2**bit) == 0:
                        bit += 1
                    if bit < self._bucket_size:
                        current = index * self._bucket_size + bit
                        if sset[-1] + 1 == current:
                            sset = (sset[0], current)
                        else:
                            subsets.append(sset)
                            sset = (current, current)
                subsets.append(sset)
                index += 1
        results = []
        for first, last in subsets:
            if first == last:
                results.append(b'%d' % first)
            else:
                results.append(b'%d-%d' % (first, last))
        return b'<%s>' % b', '.join(results)

    def total_sizeof(self):
        s = self.__sizeof__() + self._content.__sizeof__()
        for bucket in self._content:
            s += bucket.__sizeof__()
        count = self._count
        if count:
            return (s, s/count)
        else:
            return (s, None)
