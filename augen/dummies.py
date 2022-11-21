# -*- coding: utf-8 -*-
"""
Dummy classes for integrating Acoular with Amiet Tools.
=================
@Author: Michael Markus Ackermann
"""

from acoular import PowerSpectra
from traits.api import CArray, Int


class DummyPowerSpectra(PowerSpectra):
    """Dummy class for acoular.PowerSpectra. Used to make it possible the usage
    of data generated with amiet_tools with the Acoular toolbox.

    Returns:
        DummyPowerSpectra instance.
    """

    csm = CArray()
    numchannels = Int()
    ind_high = Int()
    ind_low = Int()
    calib = None
