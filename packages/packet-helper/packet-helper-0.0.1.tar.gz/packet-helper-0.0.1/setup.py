# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="packet-helper",
    description="Several features that should help you use Scapy",
    long_description="""Use `scapy-helper <https://pypi.org/project/scapy-helper/>` instead.""",    # noqa
    version="0.0.1",
    author="Nex Sabre",
    author_email="nexsabre@protonmail.com",
    url="https://github.com/NexSabre/scapy_helper",
    license="MIT",
    packages=find_packages(),
    install_requires=['scapy-helper'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)