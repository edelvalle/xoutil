=====================================================================
:mod:`xoutil.subprocess` - Extensions to `subprocess` stardard module
=====================================================================

.. module:: xoutil.subprocess

.. versionadded:: 1.2.1

This module contains extensions to the `subprocess` standard library module. It
may be used as a replacement of the standard.

.. function:: call_and_check_output(args, *, stdin=None, shell=False)

   This function combines the result of both `call` and `check_output` (from
   the standard library module).

   Returns a tuple ``(retcode, output, err_output)``.

