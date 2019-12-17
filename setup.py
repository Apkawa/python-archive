import os
import sys

from setuptools import setup

VERSION = '0.3.0'

if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

if sys.argv[1] == 'bumpversion':
    print("bumpversion")
    try:
        part = sys.argv[2]
    except IndexError:
        part = 'patch'

    os.system("bumpversion --config-file setup.cfg %s" % part)
    os.system("git push --tags")
    sys.exit()

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Topic :: System :: Archiving',
    'Topic :: System :: Software Distribution',
]

setup(
    name='python-archive',
    version=VERSION,
    classifiers=CLASSIFIERS,
    author='Gary Wilson Jr.',
    author_email='gary@thegarywilson.com',
    packages=['archive'],
    url='https://github.com/gdub/python-archive',
    license='MIT License',
    description=('Simple library that provides a common interface for'
                 ' extracting zip and tar archives.'),
    long_description=open('README.rst').read(),
    install_require=[],
    tests_require=["tox", "pytest", "pep8"],
)
