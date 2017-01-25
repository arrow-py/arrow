import codecs
import os.path
import re
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from Cython.Build import cythonize
from setuptools.command.build_ext import build_ext
from distutils.extension import Extension


# them to extension names in dotted notation
def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


# generate an Extension object from its dotted name
def makeExtension(extName):
    try:
        version = sys.version_info.major
    except:
        version = 2
    extPath = extName.replace(".", os.path.sep) + ".pyx"
    return Extension(
        extName,
        [extPath],
        include_dirs=["."],   # adding the '.' to include_dirs is CRUCIAL!!
        extra_compile_arg=["-O" + str(version), "-Wall"],
        extra_link_args=['-g'],
    )


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


file_text = read(fpath('arrow/__init__.py'))
# get the list of extensions
extNames = scandir("arrow")

# and build up the set of Extension objects
extensions = cythonize([makeExtension(name) for name in extNames])

setup(
    name='arrow',
    version=grep('__version__'),
    description='Better dates and times for Python',
    long_description=read(fpath('README.rst')),
    url='https://github.com/crsmithdev/arrow/',
    author='Chris Smith',
    author_email="crsmithdev@gmail.com",
    license='Apache 2.0',
    ext_modules=extensions,
    cmdclass={'build_ext': build_ext},
    packages=['arrow'],
    zip_safe=False,
    install_requires=[
        'python-dateutil'
    ],
    test_suite="tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
