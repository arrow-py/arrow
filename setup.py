import codecs
import os.path
import re
from sys import version_info

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


file_text = read(fpath('arrow/__init__.py'))

install_requires = ['backports.functools_lru_cache',
                    'python-dateutil',
                    'simplejson']
if version_info[0] == 2 and version_info[1] == 6:
    install_requires.append('chai==0.3.1')
else:
    install_requires.append('chai')


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
    install_requires=install_requires,
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

