# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil
#----------------------------------------------------------------------
# Copyright (c) 2013, 2014 Merchise Autrement and Contributors
# Copyright (c) 2012 Medardo Rodríguez
# All rights reserved.
#
# Author: Medardo Rodriguez
# Contributors: see CONTRIBUTORS and HISTORY file
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created: Mar 23, 2012
#

'''`xoutil` is a collection of disparate utilities that does not conform
a framework for anything. `xoutil` is essentially an extension to the
Python's standard library.

xoutil provides very simple implementations of mini-frameworks for several
programming tasks. For instance the :py:mod:`xoutil.aop` provides two basic
implementations of what may be called Aspect-Oriented Programming (AOP), but
we do not claim any affiliation to other AOP frameworks. In fact, we believe
that Python's dynamic nature makes so easy the injection of code that every
team would probably use it's own AOP mini-framework.

xoutil also provides a basic implementation of :mod:`execution contexts
<xoutil.context>`, that allows a programmer to enter/exit an execution
context; which then may signal a component to behave differently. This
implementation of contexts does not support distribution, though. But it's
useful to implement components that have two different interfaces according to
the context in which they are invoked. In this regard, contexts are a thin
(but very idiomatic) alternative to some of the design patterns found
elsewhere.

'''


from ._values import Unset, Ignored
from xoutil.names import namelist
__all__ = namelist(Unset, Ignored)
del namelist
