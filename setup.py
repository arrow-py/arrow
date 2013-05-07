try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='arrow',
    version='0.2.0',
    description='Better dates and times for Python',
    url='https://github.com/crsmithdev/arrow',
    author='Chris Smith',
    author_email="chris@cir.ca",
    license='Apache 2.0',
    packages=['arrow'],
    zip_safe=False,
    install_requires=[
        'python-dateutil'
    ]
)

