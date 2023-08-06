#!/usr/bin/python
import setuptools
from physicslib import __version__

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="physicslib",
    version=__version__,
    packages=setuptools.find_packages(),
    author="NamorNiradnug",
    author_email="roma937a@mail.ru",
    license="MIT",
    url="https://github.com/NamorNiradnug/physicslib",
    description="Library with physical objects and constants.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
