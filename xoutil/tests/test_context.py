#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.test_context
#----------------------------------------------------------------------
# Copyright (c) 2013 Merchise Autrement and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under
# the terms of the LICENCE attached in the distribution package.
#
# Created on 2013-01-15

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_abs_imports)

import unittest
from xoutil.context import context

__author__ = "Manuel Vázquez Acosta <mva.led@gmail.com>"
__date__   = "Tue Jan 15 12:17:01 2013"


class TestContext(unittest.TestCase):
    def test_simple_contexts(self):
        with context('CONTEXT-1'):
            self.assertIsNot(None, context['CONTEXT-1'])
            with context('CONTEXT-1'):
                with context('context-2'):
                    self.assertIsNot(None, context['CONTEXT-1'])
                    self.assertIsNot(None, context['context-2'])
                self.assertEquals(False, bool(context['context-2']))
            self.assertIsNot(None, context['CONTEXT-1'])
        self.assertEquals(False, bool(context['CONTEXT-1']))


    def test_with_objects(self):
        CONTEXT1 = object()
        CONTEXT2 = object()
        with context(CONTEXT1):
            self.assertIsNot(None, context[CONTEXT1])
            with context(CONTEXT1):
                with context(CONTEXT2):
                    self.assertIsNot(None, context[CONTEXT1])
                    self.assertIsNot(None, context[CONTEXT2])
                self.assertEquals(False, bool(context[CONTEXT2]))
            self.assertIsNot(None, context[CONTEXT1])
        self.assertEquals(False, bool(context[CONTEXT1]))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(verbosity=2)