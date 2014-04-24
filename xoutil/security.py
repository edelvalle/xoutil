# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.security
#----------------------------------------------------------------------
# Copyright (c) 2014 Merchise Autrement
# All rights reserved.
#
# Author: Medardo Rodriguez
# Contributors: see CONTRIBUTORS and HISTORY file
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 2014-04-22

'''General security tools.

Adds the ability to generate new passwords using a source pass-phrase and a
secury strong level.

'''

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_abs_imports)


from xoutil.names import strlist as strs
__all__ = strs('PASS_PHRASE_LEVEL_BASIC',
               'PASS_PHRASE_LEVEL_MAPPED',
               'PASS_PHRASE_LEVEL_MAPPED_MIXED',
               'PASS_PHRASE_LEVEL_MAPPED_SALTED',
               'PASS_PHRASE_LEVEL_STRICT',
               'create_password')
del strs


PASS_PHRASE_LEVEL_BASIC = 0
PASS_PHRASE_LEVEL_MAPPED = 1
PASS_PHRASE_LEVEL_MAPPED_MIXED = 2
PASS_PHRASE_LEVEL_MAPPED_SALTED = 3
PASS_PHRASE_LEVEL_STRICT = 4

DEFAULT_PASS_PHRASE_LEVEL = PASS_PHRASE_LEVEL_MAPPED_SALTED

MAX_PASSWORD_SIZE = 1024


# Used to strict password generator
PYTHON_ZEN = [
    "Beautiful is better than ugly.",
    "Explicit is better than implicit.",
    "Simple is better than complex.",
    "Complex is better than complicated.",
    "Flat is better than nested.",
    "Sparse is better than dense.",
    "Readability counts.",
    "Special cases aren't special enough to break the rules.",
    "Although practicality beats purity.",
    "Errors should never pass silently.",
    "Unless explicitly silenced.",
    "In the face of ambiguity, refuse the temptation to guess.",
    "There should be one-- and preferably only one --obvious way to do it.",
    "Although that way may not be obvious at first unless you're Dutch.",
    "Now is better than never.",
    "Although never is often better than *right* now.",
    "If the implementation is hard to explain, it's a bad idea.",
    "If the implementation is easy to explain, it may be a good idea.",
    "Namespaces are one honking great idea -- let's do more of those!"]


def create_password(pass_phrase, level=DEFAULT_PASS_PHRASE_LEVEL):
    '''Generate a new password, given a source `pass-phrase` and a `level`.

    :param pass_phrase: String pass-phrase to be used as base of password
                        generation process.

    :param level: Numerical security level (the bigger the more secure, but
                  don't exaggerate!).

    If `pass_phrase` is ``None`` or an empty string, generate a secure salt
    and, in this case, `level*8` will be the desired size.  Zero means to
    leave the size uncontrolled.  "Salt" is generated by scrambling the
    concatenation of a random phrase from the zen of Python to a random number
    between `10000` and `99990` (consecutive equals characters are removed).
    A "salt" is a password not based in a pass-phrase.

    When `pass_phrase` is a valid string, `level` means a generation method.
    A selected level implies all other with an inferior numerical value.  In
    this module there are several constants definitions with numerical values
    starting with `0`:

    `PASS_PHRASE_LEVEL_BASIC`

        Generate the same pass-phrase, just removing invalid characters for
        passwords and converting the result to lower-case.

    `PASS_PHRASE_LEVEL_MAPPED`

        Replace some characters with new values: ``'e'->'3'``, ``'i'->'1'``,
        ``'o'->'0'``, ``'s'->'5'``.

    `PASS_PHRASE_LEVEL_MAPPED_MIXED`

        Consonants before 'M' (including it) are converted to upper-case, all
        other consonants are kept lower-case.

    `PASS_PHRASE_LEVEL_MAPPED_SALTED`

        Adds a suffix with the year of current date ("<YYYY>").

    `PASS_PHRASE_LEVEL_STRICT`

        Randomly scramble previous result until unbreakable password is
        obtained.  Minimal length for strict passwords is `32` because the
        resulting length is ``8*<numerical-value-of-level>`` and this constant
        is equal to `4`.  To increase desired resulting size use any number
        greater than `4`.  When the required size can't be obtained with the
        given pass-phrase, iterate adding a "salt" generated recursively with
        this same function (see above).

    Maximum size for both methods is 1024 defined in `MAX_PASSWORD_SIZE`
    constant.

    Default level is `PASS_PHRASE_LEVEL_MAPPED_SALTED` and it's the proposed
    one for the security mechanism for allowing developers to modify user's
    passwords in order to use production data-bases in development scenarios.

    '''
    from random import sample, randint
    from xoutil.string import normalize_slug
    if pass_phrase:
        # PASS_PHRASE_LEVEL_BASIC
        res = normalize_slug(pass_phrase, '', True)
        if level >= PASS_PHRASE_LEVEL_MAPPED:
            for (old, new) in ('e3', 'i1', 'o0', 's5'):
                res = res.replace(old, new)
        if level >= PASS_PHRASE_LEVEL_MAPPED_MIXED:
            for new in "BCDFGHJKLM":
                old = new.lower()
                res = res.replace(old, new)
        if level >= PASS_PHRASE_LEVEL_MAPPED_SALTED:
            from datetime import datetime
            today = datetime.today()
            res += today.strftime("%Y")
        if level >= PASS_PHRASE_LEVEL_STRICT:
            scramble = True
            size = 8*level
            while len(res) < size:
                res += create_password(None)    # salt
        else:
            scramble = False
            size = MAX_PASSWORD_SIZE
    else:
        scramble = True
        if level <= 0:
            size = MAX_PASSWORD_SIZE
        else:
            size = level*8
            if size > MAX_PASSWORD_SIZE:
                size = MAX_PASSWORD_SIZE
        res = ""
        while len(res) < size:
            phrase = PYTHON_ZEN[randint(1, len(PYTHON_ZEN)) - 1]
            phrase += str(randint(10000, 99999))
            res += normalize_slug(phrase, '', True)
    if scramble:
        res = ''.join(sample(res, len(res)))
    return res[:size]