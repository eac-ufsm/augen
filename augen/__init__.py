# -*- coding: utf-8 -*-
"""
Init file, to define the main functions and classes available, as well as the
sub-modules.
=================
@Author: Michael Markus Ackermann
"""

from . import utils
from .beamer import *
from .data import *
from .dummies import *

__all__ = [
    # Classes
    "DummyPowerSpectra",
    "SimpleBeamer",
    "EasyBeamer",
    "AmietDataReader",
    "AmietDataGenerator",
    "AmietFrequencyData",
]

__author__ = "Michael Markus Ackermann"
__date__ = "26 Juny 2022"
__version__ = "0.1.0"
