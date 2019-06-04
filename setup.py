# -*- coding: utf-8 -*-
import io
import re

from setuptools import setup

with io.open("README.rst", "r", encoding="utf-8") as f:
    readme = f.read()

with io.open("arrow/__init__.py", "r", encoding="utf-8") as f:
    init = f.read()


def get_version():
    pattern = r'{}\W*=\W*"([^"]+)"'.format("__version__")
    return re.findall(pattern, init)[0]


setup(
    name="arrow",
    version=get_version(),
    description="Better dates and times for Python",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://arrow.readthedocs.io/en/latest/",
    author="Chris Smith",
    author_email="crsmithdev@gmail.com",
    license="Apache 2.0",
    packages=["arrow"],
    zip_safe=False,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=["python-dateutil"],
    extras_require={":python_version=='2.7'": ["backports.functools_lru_cache>=1.2.1"]},
    test_suite="tests",
    tests_require=["chai"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="arrow date time datetime",
    project_urls={
        "Repository": "https://github.com/crsmithdev/arrow",
        "Bug Reports": "https://github.com/crsmithdev/arrow/issues",
    },
)
