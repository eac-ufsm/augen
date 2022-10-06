# -*- coding: utf-8 -*-
"""
Simple Beamer class testing script.
=================
@Author: Michael Markus Ackermann
"""
import acoular
from augen import AmietDataReader, SimpleBeamer

from common_functions import simple_plot

acoular.config.global_caching = "none"  # Disable caching

# Dynamic range
dr = [8.80671944193782, 8.36725794822649, 9.59651132219212]
dr = [round(x, 2) for x in dr]


teste = AmietDataReader("supplies\\AmietData_Spiral_MicArray.h5")
mic_array = acoular.MicGeom(from_file="supplies\\Spiral_MicArray.xml")

for i in range(len(teste.frequencies)):
    freq_i = teste.get_frequency_data(
        teste.frequencies[i]
    )  # Extracts the frequency data
    ageom = teste.get_airfoil()  # Extract the AirfoilGeom used
    title = f"Frequency: {freq_i.frequency} Hz \nSpiral Mic. Array"

    beam_i = SimpleBeamer(freq_i, mic_array, teste.get_grid(), 128, False, -93.98)
    level_i = beam_i.get_beamforming()
    simple_plot(ageom.b, ageom.d, title, level_i, beam_i.grid, dr[i])
