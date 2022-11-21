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
Airfoil = AmT.loadAirfoilGeom("tests\\supplies\\AirfoilGeom.json")
# Cconditions setup
Setup = AmT.loadTestSetup("tests\\supplies\\TestSetup.json")
# Microphone array
MicArray = acoular.MicGeom(from_file="tests\\supplies\\quadrangular_array.xml")

# Multiple frequencies data generation
test_data = AmietDataGenerator(
    Setup,  # Conditions setup instance
    Airfoil,  # Airfoil geomtry instance
    MicArray,  # Microphone array instance
    # Given a kc list turn into a frequency list
    frequency_by_kc([5, 10, 20], Airfoil.b, Setup.c0),
    -1,  # Distance of the array from the airfoil (pos. in z axis)
    [1.16, 1.16],  #  X and Y grid size
    [0.05, 0.05],  # Scan points spacing
    "tests\\supplies\\AmietData_QuadrangularArray4",  # data file name
    True,  # Optional: prints the steps allong the way
)
test_data.run()  # Runs the simulation and creates the data during the process
