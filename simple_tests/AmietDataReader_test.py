# -*- coding: utf-8 -*-
"""
Setup file
=================
@Author: Michael Markus Ackermann
"""
# Import needed libraries/modules/packages
from augen import AmietDataReader

teste = AmietDataReader("supplies\\AmietData_Spiral_MicArray.h5")

f0 = teste.get_frequency_data(teste.frequencies[0])
f1 = teste.get_frequency_data(teste.frequencies[2])

print(f0.frequency, f1.csm, sep="\n")
