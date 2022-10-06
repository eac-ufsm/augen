# -*- coding: utf-8 -*-
"""
Setup file
=================
@Author: Michael Markus Ackermann
"""
# Import needed libraries/modules/packages
import acoular
import amiet_tools as AmT
from augen import AmietDataGenerator
from augen.utils import frequency_by_kc

# Airfoil geometry
DARP2016Airfoil = AmT.loadAirfoilGeom("supplies\\DARP2016_AirfoilGeom.json")
# Cconditions setup
DARP2016Setup = AmT.loadTestSetup("supplies\\DARP2016_TestSetup.json")
# Microphone array
MicArray = acoular.MicGeom(from_file="supplies\\Spiral_MicArray.xml")

# Multiple frequencies data generation
test_data = AmietDataGenerator(
    DARP2016Setup,  # Conditions setup instance
    DARP2016Airfoil,  # Airfoil geomtry instance
    MicArray,  # Microphone array instance
    # Given a kc list turn into a frequency list
    frequency_by_kc([5, 10, 20], DARP2016Airfoil.b, DARP2016Setup.c0),
    -0.49,  # Distance of the array from the airfoil (pos. in z axis)
    [0.65, 0.65],  #  X and Y grid size
    [0.01, 0.01],  # Scan points spacing
    "AmietData_Spiral_MicArray_test",  # data file name
    True,  # Optional: prints the steps allong the way
)
test_data.run()  # Runs the simulation and creates the data during the process
