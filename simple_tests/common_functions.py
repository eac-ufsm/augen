# -*- coding: utf-8 -*-
"""
Common functions used in EasyBeamer_test.py and SimpleBeamer_test.py.
=================
@Author: Michael Markus Ackermann
"""

import numpy as np
from augen.utils import draw_airfoil
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def predefined_imshow(
    plt,
    level,
    grid,
    drange: float = 15,
    origin: str = "lower",
    interpolation: str = "bicubic",
    r=False,
) -> None:
    """Predefined matplotlib.pyplot.imshow().

    Args:
        plt: matplotlib.pyplot or subplot axes.
        level (List[float]): The sound pressure level calculated for the
            beamforming.
        grid (acoular.RectGrid): Grid used for the beamforming.
        drange (float, optional): dr range. Defaults to 15.
        origin (str, optional): Origin for the plot. Defaults to 'lower'.
        interpolation (str, optional): Interpolation. Defaults to 'bicubic'.
        r (bool, optional): If should return the image. Defaults to False.

    Returns:
        If `r` is `True`, returns the image created with plt.imshow().
    """
    if r == False:
        plt.imshow(
            level,
            origin=origin,
            vmin=(level.max() - drange),
            extent=grid.extend(),
            interpolation=interpolation,
        )
        return None
    else:
        return plt.imshow(
            level,
            origin=origin,
            vmin=(level.max() - drange),
            extent=grid.extend(),
            interpolation=interpolation,
        )


def simple_plot(b, d, title, level, grid, dr, cfsize=12) -> None:
    """For plotting the conventional beamforming of a single data.

    Args:
        b (float): Airfoil geometry size.
        d (float): Airfoil geometry size.
        title (str): Figure title.
        level (List[float]): The sound pressure level calculated for the
            beamforming.
        grid (acoular.RectGrid): Grid used for the beamforming.
        cfsize (int, optional): Font size of the colorbar label.

    Returns:
        None.
    """
    fig, ax = plt.subplots(1, 1, figsize=(7, 5.85))
    # Adds the title of the image
    fig.suptitle(title)  # Sets the title.
    draw_airfoil(ax, b, d)  # Draws the airfoil.
    im = predefined_imshow(ax, level, grid, r=True, drange=dr)
    # Adding labels for the axis.
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation="vertical")
    cbar.set_label("normalized dB", fontsize=cfsize)
    cbar.set_ticks(np.linspace(level.max() - dr, level.max(), int(dr)))
    cbar.set_ticklabels(
        [str(round(n, 2)) for n in np.linspace(level.max() - dr, level.max(), int(dr))]
    )
    # Label for the colorbar.
    plt.tight_layout()  # Tights the figure.
    plt.show()
    return None
