
|PyPi| |Build Status| |Codecov| |Requirements Status| |PyUP| |Python Versions| |License|


==============
python-archive
==============


This package provides a simple, pure-Python interface for handling various
archive file formats.  Currently, archive extraction is the only supported
action.  Supported file formats include:

* Zip formats and equivalents: ``.zip``, ``.egg``, ``.jar``.
* Tar and compressed tar formats: ``.tar``, ``.tar.gz``, ``.tgz``,
  ``.tar.bz2``, ``.tz2``.

python-archive is compatible and tested with Python versions 2.7, >=3.5


Example usage
=============

Using the ``Archive`` class::

    from archive import Archive

    a = Archive('files.tar.gz')
    a.extract()

Using the ``extract`` convenience function::

    from archive import extract
    # Extract in current directory.
    extract('files.tar.gz')
    # Extract in directory 'unpack_dir'.
    extract('files.tar.gz', 'unpack_dir')

By default, an ``archive.UnsafeArchive`` exception will be raised if any
file(s) in the archive would be unpacked outside of the target directory
(e.g. the archive contains absolute paths or relative paths that navigate up
and out of the target directory).  If you can trust the source of your archive
files, then it's possible to override this behavior, e.g.::

    extract('files.tar.gz', method='insecure')


More examples
-------------
Passing a file-like object is also supported::

    f = open('files.tar.gz', 'rb')
    Archive(f).extract()

If a file does not have the correct extension, or is not recognized correctly,
you may try explicitly specifying an extension (with leading period)::

    Archive('files.wrongext', ext='.tar.gz').extract()
    # or
    extract('files.wrongext', ext='.tar.gz')


Similar tools
=============

* http://pypi.python.org/pypi/patool/ - portable command line archive file
  manager.
* http://pypi.python.org/pypi/gocept.download/ - zc.buildout recipe for
  downloading and extracting an archive.

.. |PyPi| image:: https://img.shields.io/pypi/v/python-archive.svg
   :target: https://pypi.python.org/pypi/python-archive
.. |Build Status| image:: https://travis-ci.org/Apkawa/python-archive.svg?branch=master
   :target: https://travis-ci.org/Apkawa/python-archive
.. |Codecov| image:: https://codecov.io/gh/Apkawa/python-archive/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Apkawa/python-archive
.. |Requirements Status| image:: https://requires.io/github/Apkawa/python-archive/requirements.svg?branch=master
   :target: https://requires.io/github/Apkawa/python-archive/requirements/?branch=master
.. |PyUP| image:: https://pyup.io/repos/github/Apkawa/python-archive/shield.svg
   :target: https://pyup.io/repos/github/Apkawa/python-archive
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/python-archive.svg
   :target: https://pypi.python.org/pypi/python-archive
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE
