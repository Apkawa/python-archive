import os
import tarfile
import zipfile

from .compat import is_string

__version__ = '0.3.0'


class ArchiveException(Exception):
    """Base exception class for all archive errors."""
    pass


class UnrecognizedArchiveFormat(ArchiveException):
    """Error raised when passed file is not a recognized archive format."""
    pass


class UnsafeArchive(ArchiveException):
    """
    Error raised when passed file contains paths that would be extracted
    outside of the target directory.
    """
    pass


def extract(path, to_path='', ext='', **kwargs):
    """
    Unpack the tar or zip file at the specified path to the directory
    specified by to_path.
    """
    Archive(path, ext=ext).extract(to_path, **kwargs)


class Archive(object):
    """
    The external API class that encapsulates an archive implementation.
    """

    def __init__(self, file, ext=''):
        """
        Arguments:
        * 'file' can be a string path to a file or a file-like object.
        * Optional 'ext' argument can be given to override the file-type
          guess that is normally performed using the file extension of the
          given 'file'.  Should start with a dot, e.g. '.tar.gz'.
        """
        self._archive = self._archive_cls(file, ext=ext)(file)

    @staticmethod
    def _archive_cls(file, ext=''):
        """
        Return the proper Archive implementation class, based on the file type.
        """
        cls = None
        filename = None
        if is_string(file):
            filename = file
        else:
            try:
                filename = file.name
            except AttributeError:
                raise UnrecognizedArchiveFormat(
                    "File object not a recognized archive format.")
        lookup_filename = filename + ext
        base, tail_ext = os.path.splitext(lookup_filename.lower())
        cls = extension_map.get(tail_ext)
        if not cls:
            base, ext = os.path.splitext(base)
            cls = extension_map.get(ext)
        if not cls:
            raise UnrecognizedArchiveFormat(
                "Path not a recognized archive format: %s" % filename)
        return cls

    def extract(self, *args, **kwargs):
        self._archive.extract(*args, **kwargs)

    def list(self):
        self._archive.list()


class BaseArchive(object):
    """
    Base Archive class.  Implementations should inherit this class.
    """

    def __del__(self):
        if hasattr(self, "_archive"):
            self._archive.close()

    def list(self):
        raise NotImplementedError()

    def filenames(self):
        """
        Return a list of the filenames contained in the archive.
        """
        raise NotImplementedError()

    def _extract(self, to_path):
        """
        Performs the actual extraction.  Separate from 'extract' method so that
        we don't recurse when subclasses don't declare their own 'extract'
        method.
        """
        self._archive.extractall(to_path)

    def extract(self, to_path='', method='safe'):
        if method == 'safe':
            self.check_files(to_path)
        elif method == 'insecure':
            pass
        else:
            raise ValueError("Invalid method option")
        self._extract(to_path)

    def check_files(self, to_path=None):
        """
        Check that all of the files contained in the archive are within the
        target directory.
        """
        if to_path:
            target_path = os.path.normpath(os.path.realpath(to_path))
        else:
            target_path = os.getcwd()
        for filename in self.filenames():
            extract_path = os.path.join(target_path, filename)
            extract_path = os.path.normpath(os.path.realpath(extract_path))
            if not extract_path.startswith(target_path):
                raise UnsafeArchive(
                    "Archive member destination is outside the target"
                    " directory.  member: %s" % filename)


class TarArchive(BaseArchive):

    def __init__(self, file):
        # tarfile's open uses different parameters for file path vs. file obj.
        if is_string(file):
            self._archive = tarfile.open(name=file)
        else:
            self._archive = tarfile.open(fileobj=file)

    def list(self, *args, **kwargs):
        self._archive.list(*args, **kwargs)

    def filenames(self):
        return self._archive.getnames()


class ZipArchive(BaseArchive):

    def __init__(self, file):
        # ZipFile's 'file' parameter can be path (string) or file-like obj.
        self._archive = zipfile.ZipFile(file)

    def list(self, *args, **kwargs):
        self._archive.printdir(*args, **kwargs)

    def filenames(self):
        return self._archive.namelist()

    def _extract_file(self, info, to_path):
        out_path = self._archive.extract(info.filename, path=to_path)

        permissions = info.external_attr >> 16

        # If no specific file permissions are specified we use the
        # default used by Python when creating the files.
        if permissions:
            os.chmod(out_path, permissions)

    def _extract(self, to_path):
        """
        Overrides the BaseArchive _extract method. For zip files we need
        to take special care to perserve file permissions:

        burgundywall.com/post/preserving-file-perms-with-python-zipfile-module

        """
        for info in self._archive.infolist():
            self._extract_file(info=info, to_path=to_path)


extension_map = {
    '.docx': ZipArchive,
    '.egg': ZipArchive,
    '.jar': ZipArchive,
    '.odg': ZipArchive,
    '.odp': ZipArchive,
    '.ods': ZipArchive,
    '.odt': ZipArchive,
    '.pptx': ZipArchive,
    '.tar': TarArchive,
    '.tar.bz2': TarArchive,
    '.tar.gz': TarArchive,
    '.tgz': TarArchive,
    '.tz2': TarArchive,
    '.xlsx': ZipArchive,
    '.zip': ZipArchive,
}
