import codecs
import os.path
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


def grep(attrname):
    pattern = r"{}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


file_text = read(fpath('arrow/__init__.py'))

setup(
    name='arrow',
    version=grep('__version__'),
    description='Better dates and times for Python',
    long_description=read(fpath('README.rst')),
    url='https://github.com/crsmithdev/arrow/',
    author='Chris Smith',
    author_email="crsmithdev@gmail.com",
    license='Apache 2.0',
    packages=['arrow'],
    zip_safe=False,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
    install_requires=[
        'python-dateutil',
    ],
    extras_require={
        ":python_version=='2.7'": ['backports.functools_lru_cache>=1.2.1'],
    },
    test_suite="tests",
    tests_require=['chai'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
