# -*- coding: utf-8 -*-
"""
Setup file
=================
@Author: Michael Markus Ackermann
"""

from setuptools import setup

settings = {
    "name": "augen",
    "version": "0.1.1",
    "description": "Amiet-Acoular Integration Module in Python",
    "url": "https://github.com/eac-ufsm/augen",
    "author": "Michael Markus Ackermann",
    "author_email": "michael.ackermann@eac.ufsm.br",
    "license": "MIT",
    "install_requires": [
        "acoular>=21.5",
        "amiet-tools>=0.0.2",
        "numpy>=1.20.3",
        "scipy>=1.7.1",
    ],
    "packages": ["augen", "augen.utils"],
}

setup(**settings)
