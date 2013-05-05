try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='arrow',
    version='0.1.6',
    description="Sensible dates for Python",
    url='https://github.com/crsmithdev/arrow',
    author='Chris Smith',
    author_email="chris@cir.ca",
    license='MIT',
    packages=['arrow'],
    zip_safe=False,
    install_requires=[
        'python-dateutil'
    ]
)