This is the last release of the 1.6 series.  It's being synchronized with
release 1.7.0 to deprecate here what's being changed there.

- The `defaults` argument of `xoutil.objects.smart_copy`:func: is marked to be
  keyword-only in version 1.7.0.

- Fixes a bug in `xoutil.objects.smart_copy`:func:.  If `defaults` was None is
  was not being treated the same as being False, as documented.  This bug was
  also fixed in version 1.7.0.
