from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="chinese_name",
    version="0.0.1",
    author="echo kang",
    author_email="528507274@qq.com",
    description="gen chinese name",
    long_description=open("README.md").read(),
    license="MIT",
    url="http://xx.com",
    packages=['src'],
    install_requires=[

    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)