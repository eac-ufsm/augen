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


"""
# UNSUDED CLASS.
# REASON: ERROR RELATED TO GETTING THE steer_vector FROM THE OBJECT!
# BREAKS WITH bb = acoular.BeamformingBase() -> bb.synthetic(frequency)
class DummySteeringVector(SteeringVector):
    #Dummy for acoular.SteeringVector

    def __init__(self, steer_vector, grid, mics):
        super().__init__()
        self._steer_vector = steer_vector
        self.grid = grid
        self.mics = mics

    def steer_vector(self):
        #Getter for the steering vector.

        #Returns:
        #    List[complex]: array of shape (ngridpts, nmics) containing
        #        the steering vectors for the given frequency.
        return self._steer_vector
"""
