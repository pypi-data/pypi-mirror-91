#!/usr/bin/env python
import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="esteira",
    version="1.0.0",
    author="Guilherme Isaías",
    author_email="guilherme@guilhermeweb.dev",
    description="A open source automation server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guilhermewebdev/esteira",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'docker',
        'gitpython',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
