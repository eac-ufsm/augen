# -*- coding: utf-8 -*-
"""
XML utilities.
=================
@Author: Michael Markus Ackermann
"""


def xml_save_array(fname: str, data: str) -> None:
    """Save a .xml file.

    Args:
        fname (str): file name.
        data (str): data to be saved in the xml, already formated.

    Returns:
        None.
    """
    if ".xml" not in fname:
        fname = fname + ".xml"
    with open(fname, "w", encoding="utf-8") as file:
        file.write(data)
        file.close()
    return None


def xml_format_array(array: list, name: str) -> str:
    """Transforms an array of floats into a .xml formatation.

    Args:
        array (list): List of microphone locations [[X, n], [Y, n], [Z, n]].
        name (str): Name of microphone array.

    Returns:
        (str): Acoulars microphone geometry XML formated array.
    """
    points = '<pos\tName="Point {i}"\tx="{x}"\ty="{y}"\tz="{z}" />\n'
    points = "".join(
        points.format(i=i + 1, x=array[0][i], y=array[1][i], z=array[2][i])
        for i in range(len(array[0]))
    )
    xml = f'<?xml version="1.0" encoding="utf-8"?>\n<MicArray name="{name}">\n{points}</MicArray>'
    return xml
