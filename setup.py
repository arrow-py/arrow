try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [r for r in map(str.strip, open('requirements.txt').readlines())]

setup(
    name='arrow',
    version='0.1.0',
    author='Chris Smith',
    author_email="chris@cir.ca",
    packages=['arrow'],
    url='https://github.com/crsmithdev/arrow',
    license='LICENSE.txt',
    description="sensible dates for Python",
    keywords=['python'],
    install_requires=requirements
)