try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = "will be set by next line"
exec(open("arrow/version.py").read())

setup(
    name='arrow',
    version=__version__,
    description='Better dates and times for Python',
    url='http://crsmithdev.com/arrow',
    author='Chris Smith',
    author_email="crsmithdev@gmail.com",
    license='Apache 2.0',
    packages=['arrow'],
    zip_safe=False,
    install_requires=[
        'python-dateutil'
    ],
    test_suite="tests",
)
