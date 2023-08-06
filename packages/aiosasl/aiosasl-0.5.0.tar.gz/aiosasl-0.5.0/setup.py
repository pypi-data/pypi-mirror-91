#!/usr/bin/env python3
import os.path
import runpy

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

version_mod = runpy.run_path("aiosasl/version.py")

setup(
    name="aiosasl",
    version=version_mod["__version__"],
    description="Pure-python, protocol agnostic SASL library for asyncio",
    long_description=long_description,
    url="https://github.com/horazont/aiosasl",
    author="Jonas Wielicki",
    author_email="jonas@wielicki.name",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    keywords="asyncio sasl library",
    packages=find_packages(exclude=["tests*"])
)
