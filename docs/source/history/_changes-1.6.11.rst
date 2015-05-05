This is the last release of the 1.6 series.  It's being synchronized with
release 1.7.0 to deprecate here what's being changed there.

- The `defaults` argument of `xoutil.objects.smart_copy`:func: is going to be
  keyword-only in version 1.7.0.  Using it as a positional argument will now
  issue a warning.

- Fixes a bug in `xoutil.objects.smart_copy`:func:.  If `defaults` was None is
  was not being treated the same as being False, as documented.  This bug was
  also fixed in version 1.7.0.

- This release will be the last to support Python 3.1, 3.2 and 3.3.  Support
  will be kept for Python 2.7 and Python 3.4.

- There's a new `xoutil.eight`:mod: in xoutil 1.7.0 that will contain what's
  being left in xoutil about Python 2/3 compatibility.  Since 1.6.6 we
  un-bundled six but kept the `xoutil.six` namespace around.  This will be
  removed.
