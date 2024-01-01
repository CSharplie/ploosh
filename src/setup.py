"""Setup PyPi module"""
from setuptools import setup, find_packages

setup (
    name = "ATF",
    version = "0.0.1",
    platforms="Any",
    python_requires=">=3.6",
    license= "Apache License 2.0",
    packages = find_packages(),
)