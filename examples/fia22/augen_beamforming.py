# coding: utf-8
"""
Script used to apply the BF to the AmietData for the Circular and Spiral Array.
=================
@Author: Michael Markus Ackermann
"""
import acoular
import matplotlib.pyplot as plt
from augen import AmietDataReader, EasyBeamer
from augen.utils import draw_airfoil
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numpy import linspace

from common_functions import (
    conventional_bf,
    get_frequency_data,
    predefined_colormesh,
    predefined_imshow,
)

# Turning caching of acoular OFF
acoular.config.global_caching = "none"

# Adjusting general plotting configurations
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["font.serif"] = "Times New Roman"
plt.rcParams.update({"font.size": 16})

h5_file_loc = [
    "supplies\\AmietData_Circular_MicArray.h5",
    "supplies\\AmietData_Spiral_MicArray.h5",
]
save_file = ["Circular_MicArray", "Spiral_MicArray"]
array_name = ["Circular", "Spiral"]
dynamics = [
    [7.23579473196707, 7.76503790043174, 7.86680849023434],
    [8.80671944193782, 8.36725794822649, 9.59651132219212],
]

for j in range(len(h5_file_loc)):
    # Reading the data
    arr = AmietDataReader(h5_file_loc[j])

    # Extracting RectGrid and AirfoilGeom object
    grid, airfoil = arr.get_grid(), arr.get_airfoil()

    # -93.98 to adjust maxium value to 0
    arr_beamer = EasyBeamer(arr, 128, False, -93.98)  # With diagonal
    arr_beamer_T = EasyBeamer(arr, 128, True, -93.98)  # Without diagonal

    freqs = arr_beamer.frequencies  # Frequencies list

    # Dynamic ranges
    array_dr = dynamics[j]
    array_dr = [round(x, 2) for x in array_dr]  # Rounds the values

    # Beamformings with the diagonal
    # 1803 Hz
    arr_1_803 = arr_beamer.get_beamforming(freqs[0])
    # 3607 Hz
    arr_3_607 = arr_beamer.get_beamforming(freqs[1])
    # 7215 Hz
    arr_7_215 = arr_beamer.get_beamforming(freqs[2])

    arr_maps = [arr_1_803, arr_3_607, arr_7_215]

    # Beamformings without the diagonal
    # 1803 Hz
    arr_1_803_T = arr_beamer_T.get_beamforming(freqs[0])
    # 3607 Hz
    arr_3_607_T = arr_beamer_T.get_beamforming(freqs[1])
    # 7215 Hz
    arr_7_215_T = arr_beamer_T.get_beamforming(freqs[2])

    arr_maps_T = [arr_1_803_T, arr_3_607_T, arr_7_215_T]

    # Applies beamforming for each frequency
    xs, ys, apls = [], [], []
    for f in freqs:
        csm, w = get_frequency_data(h5_file_loc[j], freqs, f)
        x, y, apl = conventional_bf(w, csm)
        xs.append(x)
        ys.append(y)
        apls.append(apl)

    # Strings
    ftitles = []
    for f in freqs:
        ftitles.append(f"Frequency: {str(f)} Hz\nAmiet Tools - with diagonal")

    xlb = "$x$ (m)"
    ylb = "$y$ (m)"
    clb = "normalized dB"

    # Ticks for X and Y axis
    xyticks = [-0.3, -0.15, 0, 0.15, 0.3]

    # Defining figure
    fig, axs = plt.subplots(3, 3, sharex=False, sharey=False, figsize=(12, 10.5))

    plt.suptitle(f"{array_name[j]} Microphone Array", fontweight="bold")
    (axs1, axs2, axs3) = axs  # Rows 1, 2 e 3
    (ax11, ax12, ax13) = axs1  # Row 1
    (ax21, ax22, ax23) = axs2  # Row 2
    (ax31, ax32, ax33) = axs3  # Row 3

    for i in range(len(axs1)):
        # Draws the airfoil on the beamforming images
        # Row 1
        draw_airfoil(axs1[i], airfoil.b, airfoil.d, fsize="10")
        # Row 2
        draw_airfoil(axs2[i], airfoil.b, airfoil.d, fsize="10")
        # Row 3
        draw_airfoil(axs3[i], airfoil.b, airfoil.d, fsize="10")

        # TICKS X and Y
        axs1[i].axis("equal")
        # Row 1
        axs1[i].set_xticks(xyticks)
        axs1[i].set_yticks(xyticks)
        # Row 2
        axs2[i].set_xticks(xyticks)
        axs2[i].set_yticks(xyticks)
        # Row 3
        axs3[i].set_xticks(xyticks)
        axs3[i].set_yticks(xyticks)

        # LABELS X and Y
        # Row 1
        axs1[i].set_xlabel(xlb, fontsize=12)
        axs1[i].set_ylabel(ylb, fontsize=12)
        # Row 2
        axs2[i].set_xlabel(xlb, fontsize=12)
        axs2[i].set_ylabel(ylb, fontsize=12)
        # Row 3
        axs3[i].set_xlabel(xlb, fontsize=12)
        axs3[i].set_ylabel(ylb, fontsize=12)

        # TICKS X and Y
        # Row 1
        axs1[i].xaxis.set_tick_params(labelsize=12)
        axs1[i].yaxis.set_tick_params(labelsize=12)
        # Row 2
        axs2[i].xaxis.set_tick_params(labelsize=12)
        axs2[i].yaxis.set_tick_params(labelsize=12)
        # Row 3
        axs3[i].xaxis.set_tick_params(labelsize=12)
        axs3[i].yaxis.set_tick_params(labelsize=12)

        # TITLES
        axs1[i].set_title(ftitles[i], fontsize=16)
        axs2[i].set_title("Acoular - with diagonal", fontsize=16)
        axs3[i].set_title("Acoular - without diagonal", fontsize=16)

        # Images
        # Row 2
        im_top = predefined_imshow(
            axs2[i], arr_maps[i], grid, array_dr[i], interpolation="nearest", r=True
        )
        div_top = make_axes_locatable(axs2[i])
        cax_top = div_top.append_axes("right", size="5%", pad=0.05)
        cbar_top = fig.colorbar(im_top, cax=cax_top, orientation="vertical")
        cbar_top.set_label(clb, fontsize=12)
        cbar_top.set_ticks(
            linspace(arr_maps[i].max() - array_dr[i], arr_maps[i].max(), 5)
        )
        cbar_top.set_ticklabels(
            [
                str(round(n, 2)).replace(".", ",")
                for n in linspace(arr_maps[i].max() - array_dr[i], arr_maps[i].max(), 5)
            ]
        )
        cbar_top.ax.tick_params(labelsize=12)

        # Row 3
        im_middle = predefined_imshow(
            axs3[i], arr_maps_T[i], grid, array_dr[i], interpolation="nearest", r=True
        )
        div_middle = make_axes_locatable(axs3[i])
        cax_middle = div_middle.append_axes("right", size="5%", pad=0.05)
        cbar_middle = fig.colorbar(im_middle, cax=cax_middle, orientation="vertical")
        cbar_middle.set_label(clb, fontsize=12)

        cbar_middle.set_ticks(
            linspace(arr_maps_T[i].max() - array_dr[i], arr_maps_T[i].max(), 5)
        )
        cbar_middle.set_ticklabels(
            [
                str(round(n, 2)).replace(".", ",")
                for n in linspace(
                    arr_maps_T[i].max() - array_dr[i], arr_maps_T[i].max(), 5
                )
            ]
        )
        cbar_middle.ax.tick_params(labelsize=12)

        # Row 1
        im_bottom = predefined_colormesh(
            axs1[i], xs[i], ys[i], apls[i], array_dr[i], "nearest", r=True
        )
        div_bottom = make_axes_locatable(axs1[i])
        cax_bottom = div_bottom.append_axes("right", size="5%", pad=0.05)
        cbar_bottom = fig.colorbar(im_bottom, cax=cax_bottom, orientation="vertical")
        cbar_bottom.set_label(clb, fontsize=12)

        cbar_bottom.set_ticks(linspace(-array_dr[i], 0, 5))
        cbar_bottom.set_ticklabels(
            [str(round(n, 2)).replace(".", ",") for n in linspace(-array_dr[i], 0, 5)]
        )
        cbar_bottom.ax.tick_params(labelsize=12)

    plt.tight_layout()
    plt.savefig(
        f"images\\{save_file[j]}.pdf", bbox_inches="tight", pad_inches=0, dpi=600
    )
    plt.show()
    plt.close()
