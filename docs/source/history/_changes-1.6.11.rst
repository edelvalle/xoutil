This is the last release of the 1.6 series.  It's being synchronized with
release 1.7.0 to deprecate here what's being changed there.

In 1.7.0 we extract the Python 2/3 compatibility layer to a separate
`xoutil.eight`:mod: module, thus leaving ``xoutil`` modules for things that,
though they will work in both Python 2/3, are not backports or fixes to
modules in the standard library, the later will be the goal of
``xoutil.eight``.

In this regard, both 1.6.11 and 1.7.0 will be the middle ground of this
process.  Some things are deprecated in this release and removed in 1.7.0,
while others are being deprecated in 1.7.0 and removed later on.

- The `defaults` argument of `xoutil.objects.smart_copy`:func: is going to be
  keyword-only in version 1.7.0.  Using it as a positional argument will now
  issue a warning.

- Fixes a bug in `xoutil.objects.smart_copy`:func:.  If `defaults` was None is
  was not being treated the same as being False, as documented.  This bug was
  also fixed in version 1.7.0.

- This release will be the last to support Python 3.1, 3.2 and 3.3.  Support
  will be kept for Python 2.7 and Python 3.4.

- Mark the `xoutil.six`:mod: for removal in 1.7.0.
