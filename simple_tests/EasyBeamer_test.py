# -*- coding: utf-8 -*-
"""
EasyBeamer class testing script
=================
@Author: Michael Markus Ackermann
"""

import acoular
from augen import AmietDataReader, EasyBeamer

from common_functions import simple_plot

acoular.config.global_caching = "none"  # Disable caching

# Dynamic range
dr = [8.80671944193782, 8.36725794822649, 9.59651132219212]
dr = [round(x, 2) for x in dr]

teste = AmietDataReader("supplies\\AmietData_Spiral_MicArray.h5")


for i in range(len(teste.frequencies)):
    frequency = teste.frequencies[i]
    ageom = teste.get_airfoil()  # Extract the AirfoilGeom used
    title = f"Frequency: {frequency} Hz \nSpiral Mic. Array"

    beam_i = EasyBeamer(teste, 128, True, -93.98)
    level_i = beam_i.get_beamforming(frequency)
    simple_plot(ageom.b, ageom.d, title, level_i, beam_i.grid, dr[i])
