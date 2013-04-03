#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.tests.test_modules
#----------------------------------------------------------------------
# Copyright (c) 2013 Merchise Autrement and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under
# the terms of the LICENCE attached in the distribution package.
#
# Created on 2013-01-28

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_abs_imports)

import sys
import unittest

from xoutil.modules import customize, modulemethod, moduleproperty

__author__ = "Manuel Vázquez Acosta <mva.led@gmail.com>"
__date__   = "Mon Jan 28 19:32:00 2013"


class TestModulesCustomization(unittest.TestCase):
    def setUp(self):
        import testbed
        self.testbed = testbed

    def tearDown(self):
        sys.modules[self.testbed.__name__] = self.testbed

    def test_echo(self):
        import testbed
        module, created, klass = customize(testbed)
        self.assertTrue(created)
        self.assertEqual(10, module.echo(10))

    def test_module_props(self):
        @property
        def this(self):
            return self

        import testbed
        module, created, klass = customize(testbed, this=this)
        self.assertTrue(created)
        self.assertEqual(module, module.this)


class TestModuleDecorators(unittest.TestCase):
    def test_echo_module_level(self):
        import sys

        @modulemethod
        def echo(self, *args):
            return (self, args)

        current_module = sys.modules[__name__]
        self.assertEquals((current_module, (1, 2)), echo(1, 2))


    def test_moduleproperties(self):
        import customizetestbed as m
        self.assertIs(m, m.this)
        self.assertIs(None, m.store)
        m.store = (1, 2)
        self.assertEquals((1, 2), m.store)
        self.assertEquals((1, 2), m._store)