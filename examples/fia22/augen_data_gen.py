# -*- coding: utf-8 -*-
"""
Script used to generate the simulated data using amiet_tools
=================
@Author: Michael Markus Ackermann
"""
# Import all needed functions and classes
from acoular import MicGeom
from amiet_tools import loadAirfoilGeom, loadTestSetup
from augen import AmietDataGenerator
from augen.utils import frequency_by_kc

# Load simulation config. files
DARP2016Airfoil = loadAirfoilGeom("supplies\\DARP2016_AirfoilGeom.json")
DARP2016Setup = loadTestSetup("supplies\\DARP2016_TestSetup.json")

# Import array geometries
circular = MicGeom(from_file="supplies\\Circular_MicArray.xml")
spiral = MicGeom(from_file="supplies\\Spiral_MicArray.xml")

mics = [spiral, circular]  # List with MicGeom objects

for mic in mics:
    # File name with path to save it
    main_name = "Circular"
    if mic is spiral:
        main_name = "Spiral"
    fname_wpath = f"supplies\\AmietData_{main_name}_MicArray"

    # Generate AmietData
    AmData = AmietDataGenerator(
        DARP2016Setup,  # Simulation general config.
        DARP2016Airfoil,  # Airfoil config.
        mic,  # MicGeom
        frequency_by_kc(
            [5, 10, 20],  # Calculates frequencies for the given kc's
            DARP2016Airfoil.b,  # Airfoil chordwise size
            DARP2016Setup.c0,  # Speed of sound in air for the simulation
        ),
        -0.49,  # Custom height
        [0.65, 0.65],  # Grid size for x and y
        [0.01, 0.01],  # Grid spacing
        fname_wpath,  # File name with path to save
        True,  # Enables console current step notice
    )
    AmData.run()  # Run simulation
