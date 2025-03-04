=========
Changelog
=========


In Development
==============
* Preserving file permissions when using zip files.
* Update tox.ini to not use a specific pypi index server. Removed support
  for Python 2.6.
* Allow for stripping/removing comments (needed by certain tools which
  bundle python-archive)
* Use relative import to allow module relocation.
* Moved tests outside of the archive package directory.
* Added Travis-CI
* Added Codecov

Version 0.2 - 2012-07-12
========================
* Added Python 3 compatibility.
* Added support for passing file-like objects instead of just a file path.
* Added the ability to override the file-type guess performed using a file's
  extension.
* Added security check when extracting to ensure a file will not get extracted
  outside of the target directory.  This is the new default behavior, though
  the check can be disabled if needed.


Version 0.1 - 2010-07-27
========================
* Initial release.
* Support for extracting zip and tar files.
