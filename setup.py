# mypy: ignore-errors
from pathlib import Path

from setuptools import setup

readme = Path("README.rst").read_text(encoding="utf-8")
version = Path("arrow/_version.py").read_text(encoding="utf-8")
about = {}
exec(version, about)

setup(
    name="arrow",
    version=about["__version__"],
    description="Better dates & times for Python",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://arrow.readthedocs.io",
    author="Chris Smith",
    author_email="crsmithdev@gmail.com",
    license="Apache 2.0",
    packages=["arrow"],
    package_data={"arrow": ["py.typed"]},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "python-dateutil>=2.7.0",
        "typing_extensions; python_version<'3.8'",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="arrow date time datetime timestamp timezone humanize",
    project_urls={
        "Repository": "https://github.com/arrow-py/arrow",
        "Bug Reports": "https://github.com/arrow-py/arrow/issues",
        "Documentation": "https://arrow.readthedocs.io",
    },
)
