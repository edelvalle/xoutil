# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.decorator
#----------------------------------------------------------------------
# Copyright (c) 2009-2011 Merchise Autrement
#
# Author: Medardo Rodriguez
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


'''Some usefull decorators.'''

# TODO: reconsider all this module


from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import)

import sys

from collections import OrderedDict
from contextlib import nested

from xoutil.objects import nameof
from xoutil.iterators import flatten
from xoutil.functools import update_wrapper, wraps, partial
from xoutil.types import FunctionType as function
curry = partial


class AttributeAlias(object):
    '''
    Descriptor to create aliases for object attributes.
    This descriptor is mainly to be used internally by "aliases" decorator.
    '''

    def __init__(self, attr_name):
        super(AttributeAlias, self).__init__()
        self.attr_name = attr_name

    def __get__(self, instance, owner):
        return getattr(instance or owner, self.attr_name)

    def __set__(self, instance, value):
        setattr(instance, self.attr_name, value)

    def __delete__(self, instance):
        delattr(instance, self.attr_name)


def settle(**kwargs):
    '''
    Return a decorator that settle different attribute values to the
    decorated target (function or class).
    '''
    def inner(target):
        for key, value in kwargs.iteritems():
            setattr(target, key, value)
        return target
    return inner


def namer(name, **kwargs):
    '''
    Similar to "settle", but always consider first argument as "name".
    '''
    return settle(__name__=name, **kwargs)


def aliases(**kwargs):
    '''
    In a class, create an "AttributeAlias" descriptor for each definition
    as keyword argument (alias=existing_attribute).
    '''
    def inner(target):
        '''
        Direct closure decorator that settle several attribute aliases.
        '''
        assert isinstance(target, type), '"target" must be a class.'
        for alias, field in kwargs.iteritems():
            setattr(target, alias, AttributeAlias(field))
        return target
    return inner


def decorator(caller):
    '''
    Eases the creation of decorators with arguments. Normally a decorator with
    arguments needs three nested functions like this::

        def decorator(*decorator_arguments):
            def real_decorator(target):
                def inner(*args, **kwargs):
                    return target(*args, **kwargs)
                return inner
            return real_decorator

    This :function:`decorator`_ reduces the need of the first level by
    comprising both into a single function definition. However it does not
    removes the need for an ``inner`` function::

        >>> @decorator
        ... def plus(target, value):
        ...    from functools import wraps
        ...    @wraps(target)
        ...    def inner(*args):
        ...        return target(*args) + value
        ...    return inner

        >>> @plus(10)
        ... def ident(val):
        ...     return val

        >>> ident(1)
        11

    A decorator with default values for all its arguments (except, of course,
    the first one which is the decorated :param:`target`_) may be invoked without
    parenthesis::

        >>> @decorator
        ... def plus2(func, value=1, missing=2):
        ...    from functools import wraps
        ...    @wraps(func)
        ...    def inner(*args):
        ...        print(missing)
        ...        return func(*args) + value
        ...    return inner

        >>> @plus2
        ... def ident2(val):
        ...     return val

        >>> ident2(10)
        2
        11

    But (if you like) you may place the parenthesis::

        >>> @plus2()
        ... def ident3(val):
        ...     return val

        >>> ident3(10)
        2
        11

    However, this is not for free, you cannot pass a single positional argument
    which type is :obj:`types.FunctionType`_::

        >>> def p():
        ...    print('This is p!!!')
        >>> @plus2(p)
        ... def dummy():
        ...    print('This is dummy')
        Traceback (most recent call last):
            ...
        TypeError: p() takes no arguments (1 given)

    The workaround for this case is to use a keyword argument.
    '''
    @wraps(caller)
    def outer_decorator(*args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], (function, type)):
            # This tries to solve the case of missing () on the decorator::
            #
            #    @decorator
            #    def somedec(func, *args, **kwargs)
            #        ...
            #
            #    @somedec
            #    def decorated(*args, **kwargs):
            #        pass
            #
            # Notice, however, that this is not general enough, since we try
            # to avoid inspecting the calling frame to see if the () are in
            # place.
            func = args[0]
            return partial(caller, func, **kwargs)()
        elif len(args) > 0 or len(kwargs) > 0:
            def _decorator(func):
                return partial(caller, **kwargs)(*((func, ) + args))
            return _decorator
        else:
            return caller
    return outer_decorator


@decorator
def assignment_operator(func, maybe_inline=False):
    '''
    Makes a function that receives a name, and other args to be
    *assignment_operator*, meaning that it if its used in a single assignment
    statement the name will be taken from the left part of the ``=`` operator::

        >>> @assignment_operator()
        ... def test(name, *args):
        ...    return name * (len(args) + 1)

        >>> test('a', 1, 2)
        'aaa'

    (The following test fails because we can't get the source of the doctest;
    so a unit test should be provided:)

    ::
        >>> b = test(1, 2)    # doctest: +SKIP
        >>> b                 # doctest: +SKIP
        'bbb'
    '''
    import inspect
    import ast

    if not isinstance(func, function):
        raise TypeError('"func" must be a function.')

    @wraps(func)
    def inner(*args):
        filename, lineno, funcname, sourcecode_lines, index = inspect.getframeinfo(sys._getframe(1))
        try:
            sourceline = sourcecode_lines[index].strip()
            parsed_line = ast.parse(sourceline, filename).body[0]
            assert maybe_inline or isinstance(parsed_line, ast.Assign)
            if isinstance(parsed_line, ast.Assign):
                assert len(parsed_line.targets) == 1
                assert isinstance(parsed_line.targets[0], ast.Name)
                name = parsed_line.targets[0].id
            elif maybe_inline:
                assert isinstance(parsed_line, ast.Expr)
                name = None
            else:
                assert False
            return func(name, *args)
        except (AssertionError, SyntaxError):
            if maybe_inline:
                return func(None, *args)
            else:
                return func(*args)
        finally:
            del filename, lineno, funcname, sourcecode_lines, index
    return inner


@decorator
def instantiate(target, *args, **kwargs):
    '''
    Some singleton classes must be instantiated as part of its declaration
    because they represents singleton objects.

    Every argument, positional or keyword, is passed as such when invoking the
    target. The following two code samples show two cases::

       >>> @instantiate
       ... class Foobar(object):
       ...    def __init__(self):
       ...        print('Init...')
       Init...


       >>> @instantiate('test', context={'x': 1})
       ... class Foobar(object):
       ...    def __init__(self, name, context):
       ...        print('Initializing a Foobar instance with name={name!r} '
       ...              'and context={context!r}'.format(**locals()))
       Initializing a Foobar instance with name='test' and context={'x': 1}

    In all cases, Foobar remains the class, not the instance::

        >>> Foobar
        <class 'decorators.Foobar'>
    '''
    target(*args, **kwargs)
    return target


class _SynchronizedType(type):
    def __init__(self, *args, **kwargs):
        self._locks = []
        self._locks_index = OrderedDict()
        self.global_lock = self.get_lock('xoutil.synchronized.global')
        super(_SynchronizedType, self).__init__(*args, **kwargs)
        
    def get_lock(self, lock):
        from threading import RLock
        if lock not in self._locks:
            l = RLock()
            l.name = nameof(lock)
            l.index = len(self._locks) - 1
            self._locks.append(l)
            self._locks_index[lock] = len(self._locks) - 1
        return self._locks[self._locks_index[lock]]
    

class synchronized(object):
    '''
    Makes a method/function synchronized by several locks. 
    
    Locks may be:
    
    - simple strings
    - lock objects
    
    String locks are globally unique, so they are preferred over lock objects
    because it's easier to be fooled by lock objects. If no locks are provided
    a single global lock it's used. The name of this single global lock is:
    'xoutil.syncronized.global'.
    
    This decorator makes sure to acquire the locks always a defined order. So
    the following two examples are equivalent:
    
        >>> @synchronized('asd', 'lkj')
        ... def something():
        ...    pass
        
        >>> @synchronized('lkj', 'asd')
        ... def something():
        ...    pass
        
    So the following function will be executed in the context of two reentrant 
    locks::
    
        >>> @synchronized('logging', 'api')
        ... def hello(name='World'):
        ...    print('Hello %s!' % name)
        
        >>> hello()
        Hello World!
        
        # In the stderr console you may have received some logs about acquiring
        # and releasing locks. Check the asociated unit tests.
    '''
    
    __metaclass__ = _SynchronizedType

    def __init__(self, *locks):
        self.locks = self.build_locks(locks)
        self.target = None
        
    @classmethod
    def build_locks(cls, *locks):
        locks = tuple(set(flatten(locks))) # Removes duplicates
        if locks:
            for lock in (l for l in locks if l not in cls._locks_index):
                cls.get_lock(lock)
            res = [cls._locks[x] for lock, x in cls._locks_index.iteritems() if lock in locks]            
            return res
        else:
            return [cls.global_lock]

    def __call__(self, *args, **kwargs):
        if self.target is None:
            assert len(args) == 1 and not kwargs
            self.target = args[0]
            return self
        else:
            with nested(*self.locks):
                return self.target(*args, **kwargs)
            


__all__ = (b'AttributeAlias',
           b'update_wrapper',
           b'wraps',
           b'partial',
           b'settle',
           b'namer',
           b'curry',
           b'aliases',
           b'decorator',
           b'assignment_operator',
           b'instantiate')


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
