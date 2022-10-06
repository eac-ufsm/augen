# coding: utf-8
"""
Common functions for plotting figures for the FIA22 Article.
=================
@Author: Michael Markus Ackermann
"""
from amiet_tools import rect_grid
from augen.utils import index_of_value
from h5py import File
from numpy import array, log10, zeros


# Function to extract data without using the AmietDataReader
def get_frequency_data(fname, flist, frequency):
    """Extracts the data for the frequency in the given index position.

    Args:
        frequency (float): Frequency to extract.

    Returns:
        AmietFrequencyData: Object instance with the data of the frequency.
    """
    f_pos = index_of_value(flist, frequency)
    hdf = File(fname, "r")
    fq = hdf.get("Frequency data")
    freq_x = fq.get(f"freq_{f_pos}")
    steering_vector = freq_x.get("steering_vector")[()]
    raw_csm = freq_x.get("CSM")[()]
    hdf.close()
    return raw_csm, steering_vector


# Conventional beamforming algorithm
def conventional_bf(w, csm):
    scan_sides = array([0.65, 0.65])  # Scan plane side length
    scan_spacings = array([0.01, 0.01])  # Scan points spacing
    scan_xy = rect_grid(scan_sides, scan_spacings)  # Rectangular grid

    # Reshape grid points for 2D plotting
    plotting_shape = (scan_sides / scan_spacings + 1)[::-1].astype(int)
    scan_x = scan_xy[0, :].reshape(plotting_shape)
    scan_y = scan_xy[1, :].reshape(plotting_shape)

    # Number of points in the scanning grid
    npoints = scan_xy.shape[1]
    # Vector of source powers
    ap = zeros(npoints)

    for n in range(npoints):
        ap[n] = (w[:, n].conj().T @ csm @ w[:, n]).real

    # Reshape grid points for 2D plotting
    ap = ap.reshape(plotting_shape)
    return scan_x, scan_y, 10 * log10(ap / ap.max())


# Functions to facilitate plotting


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


def predefined_colormesh(
    plt,
    x,
    y,
    level,
    drange: float = 15,
    interpolation: str = "bicubic",
    r=False,
    ctmap="viridis",
) -> None:
    """Predefined matplotlib.pyplot.pcolormesh().

    Args:
        plt: matplotlib.pyplot or subplot axes.
        level (List[float]): The sound pressure level calculated for the
            beamforming.
        drange (float, optional): dr range. Defaults to 15.
        interpolation (str, optional): Interpolation. Defaults to 'bicubic'.
        r (bool, optional): If should return the image. Defaults to False.

    Returns:
        If `r` is `True`, returns the image created with plt.imshow().
    """
    if r == False:
        plt.pcolormesh(
            x,
            y,
            level,
            cmap=ctmap,
            vmax=0,
            vmin=-drange,
            shading=interpolation,
            linewidth=0,
            rasterized=True,
        )
        return None
    else:
        return plt.pcolormesh(
            x,
            y,
            level,
            cmap=ctmap,
            vmax=0,
            vmin=-drange,
            shading=interpolation,
            linewidth=0,
            rasterized=True,
        )
