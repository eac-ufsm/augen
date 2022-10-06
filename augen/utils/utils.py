# -*- coding: utf-8 -*-
"""
General utilities.
=================
@Author: Michael Markus Ackermann
"""

from typing import List

import numpy as np


def truncate(value: float, decimals: int = 0) -> float:
    """A truncation function.

    Args:
        value (float): Value to be truncated.
        decimals (int, optional): Quantity of decimals to use. Defaults to 0.

    Returns:
        float: Truncated value.
    """
    multiplier = 10 ** decimals
    return int(value * multiplier) / multiplier


def index_of_value(array: List[float] or np.ndarray, value: float or int) -> int:
    """Get the index position of the value inside the given array.

    Args:
        array (List[float] or np.ndarray): Array with values.
        value (float or int): Value to look inside the array.

    Returns:
        int: _description_
    """
    return int(np.where(array == value)[0])


def frequency_by_kc(kc: float, b: float, c0: float = 340) -> float or np.ndarray:
    """Calculates the frequency using a kc, sound speed and airfoil half chord.

    Args:
        kc (float or List[float] or numpy.ndarray): Chordwise normalised frequency.
        c0 (float): Sound speed (m).
        b (float): Airfoil half chord (m). Defaults to 340.

    Returns:
        float or List[float]: Frequency (Hz).
    """
    if type(kc) == list:
        kc = np.array(kc)

    f0 = kc * c0 / (2 * np.pi * (2 * b))
    if len(kc) == 1:
        return round(f0, 2)
    else:
        return np.array([round(f, 2) for f in f0])
