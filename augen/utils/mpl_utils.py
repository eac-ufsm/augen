# -*- coding: utf-8 -*-
"""
Functions to ease the process of creating images with Matplotlib (mpl).

Notice: Since it doesn't use directly the matplotlib library in some of the
    functions above, it doesn't mean it's broken — not using a direct link to
    matplotlib in a few case allows the code to be more generic and to work with
    a figure instance or a subplot figure axes.
=================
@Author: Michael Markus Ackermann
"""


def draw_airfoil(
    fig,
    b: float,
    d: float,
    color: str = "k",
    fsize: str = "18",
    texts: tuple = ("LE", "TE"),
) -> None:
    """Draws the airfoil on the figure.

    Args:
        fig: Figure instance.
        b (float): Airfoil geometry size.
        d (float): Airfoil geometry size.
        color (str, optional): Colors of the lines to. Defaults to 'k'.
        fsize (str, optional): Fontsize of the text. Defaults to '18'.
        texts (tuple, optional): Texts for the Leading Edge and Trailing Edge.
            Defaults to ('LE', 'TE').

    Returns:
        None.
    """
    # Y axis drawing
    fig.vlines(-b, -d, d, color=color)
    fig.vlines(b, -d, d, color=color)
    # X axis drawing
    fig.hlines(-d, -b, b, color=color)
    fig.hlines(d, -b, b, color=color)
    # Drawing text indicators
    fig.text(-b + 0.01, d - 0.05, texts[0], fontsize=fsize, color=color)
    fig.text(b + 0.01, d - 0.05, texts[1], fontsize=fsize, color=color)

    return None
