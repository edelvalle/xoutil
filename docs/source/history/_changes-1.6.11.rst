- The `defaults` argument of `xoutil.objects.smart_copy`:func: is marked to be
  keyword-only in version 1.7.0.

- Fixes a bug in `xoutil.objects.smart_copy`:func:.  If `defaults` was None is
  was not being treated the same as being False, as documented.  This bug was
  also fixed in version 1.7.0.
