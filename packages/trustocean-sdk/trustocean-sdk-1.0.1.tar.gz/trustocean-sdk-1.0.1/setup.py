# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trustocean-sdk", # replace with your own username
    version="1.0.1",
    author="TrustOcean Limited",
    author_email="jasonlong@qiaokr.com",
    description="A SDK package of TrustOcean Limited SSL API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/londry/TRUSTOCEAN-SDK-PYTHON",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)