# From itsaprounis @ https://github.com/ltsaprounis/python-project-template/blob/1c25dc7022614b59c61bb99321c580afdeac17f2/setup.py
__author__ = ["author name"]

from setuptools import setup, find_packages

setup(
    name="examplepackage",
    version="x.x",
    packages=find_packages(),
    description="package description",
    author="author name",
    install_requires=[
        "numpy>=1.0",
        "pandas==1.0",
    ],
)
