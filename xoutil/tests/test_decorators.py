#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.tests.test_decorators
#----------------------------------------------------------------------
# Copyright (c) 2011 Medardo Rodríguez
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License (GPL) as published by the
# Free Software Foundation;  either version 2  of  the  License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
# Created on Nov 18, 2011

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode)

__docstring_format__ = 'rst'
__author__ = 'manu'

import unittest
from xoutil.decorators import assignment_operator, decorator, synchronized



class TestAssignable(unittest.TestCase):
    def test_inline_expression(self):
        @assignment_operator()
        def test(name, *args):
            return name * (len(args) + 1)

        self.assertEqual('aaa', test('a', 1, 2))

    def test_assignment(self):
        @assignment_operator()
        def test(name, *args):
            return name * (len(args) + 1)

        b = test(1, 2, 4)
        self.assertEqual('bbbb', b)

    def test_regression_inline(self):
        @assignment_operator(maybe_inline=True)
        def test(name, *args):
            if name:
                return name * (len(args) + 1)
            else:
                return None

        self.assertIs(None, test('a', 1, 2))

    def test_regression_on_block(self):
        @assignment_operator(maybe_inline=True)
        def union(name, *args):
            return (name,) + args

        for which in (union(1, 2),):
            self.assertEqual((None, 1, 2), which)


    def test_argsless_decorator(self):
        @decorator
        def log(func, fmt='Calling function %s'):
            def inner(*args, **kwargs):
                print(fmt % func.__name__)
                return func(*args, **kwargs)
            return inner

        @log
        def hello(msg='Hi'):
            print(msg)

        @log()
        def hi(msg='Hello'):
            print(msg)

        hi()
        hello()
        pass

    def test_returning_argless(self):
        @decorator
        def plus2(func, value=1):
            def inner(*args):
                return func(*args) + value
            return inner

        @plus2
        def ident2(val):
            return val

        @plus2()
        def ident3(val):
            return val

        self.assertEquals(ident2(10), 11)
        self.assertEquals(ident3(10), 11)


class RegressionTests(unittest.TestCase):
    def test_with_kwargs(self):
        'When passing a function as first positional argument, kwargs should be tested empty'
        from xoutil.functools import partial
        @decorator
        def ditmoi(target, *args, **kwargs):
            return partial(target, *args, **kwargs)

        def badguy(n):
            return n

        @ditmoi(badguy, b=1)
        def foobar(n, *args, **kw):
            return n

        self.assertEqual(badguy, foobar(1))


class SynchronizedTests(unittest.TestCase):
    def test_global_order(self):
        '''
        Tests the global order of synchronized-locks to avoid deadlocks.

        For any pair of locks l1 and l2 if both are applied to two (or more)
        functions, their relative order is the always the same: if l1 < l2
        (meaning comes before) for function 1 then l1 < l2 for function 2 and
        viceversa. The dual should also hold.
        '''
        import random
        from xoutil.uuid import uuid
        from itertools import combinations
        lock_names = [uuid()[:8] for _x in range(10)]
        locks1 = random.sample(lock_names, 8)
        locks2 = random.sample(lock_names, 8)
        print(tuple(set(locks1)))
        print(tuple(set(locks2)))

        @synchronized(*locks1)
        def function1():
            return 1

        @synchronized(*locks2)
        def function2():
            return 2

        @synchronized
        def function3():
            return 3

        function1_locks = {l.name: l for l in function1.locks}
        function2_locks = {l.name: l for l in function2.locks}

        for l1, l2 in combinations(lock_names, 2):
            if l1 in function1_locks and l2 in function1_locks:
                i1 = function1_locks[l1].index
                i2 = function1_locks[l2].index
                if l1 in function2_locks and l2 in function2_locks:
                    j1 = function2_locks[l1].index
                    j2 = function2_locks[l2].index
                    self.assert_((i1 < i2) and (j1 < i2) or
                                 (i1 > i2) and (j1 > j2))

        self.assertEqual(1, function1())
        self.assertEqual(3, function3())

        function3_locks = {l.name: l for l in function3.locks}
        self.assertEqual(1, len(function3_locks))
        self.assertEquals(['xoutil.synchronized.global'], function3_locks.keys())

    def test_methods(self):
        class Foobar(object):
            @synchronized
            def method1(self, n):
                return -n

        foo = Foobar()
        self.assertEqual(-1, foo.method1(1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
