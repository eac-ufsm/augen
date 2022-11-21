import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import amiet_tools as AmT
import acoular
import locale

locale.setlocale(locale.LC_NUMERIC, 'pt_BR')
plt.rcParams['axes.formatter.use_locale'] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["font.serif"] = "Times New Roman"
plt.rcParams.update({'font.size': 16})

b = .075
d = .225

x = [-b, -b, b, b, -b+.001]
y = [d, -d, -d, d, d]
z = np.zeros(5)

m = acoular.MicGeom(
    from_file='supplies/quadrangular_array.xml')


scan_sides = np.array([.65, .65])  # scan plane side length
scan_spacings = np.array([0.05, 0.05])  # scan points spacing

scan_xy = AmT.rect_grid(scan_sides, scan_spacings)

# Reshape grid points for 2D plotting
plotting_shape = (scan_sides/scan_spacings+1)[::-1].astype(int)
scan_x = scan_xy[0, :].reshape(plotting_shape)
scan_y = scan_xy[1, :].reshape(plotting_shape)

# Número de pontos do plano
N = scan_xy.shape[1]

# Create array with (x, y, z) coordinates of the scan points
scan_xyz = np.concatenate((scan_xy, np.zeros((1, N))))

# %% *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# Plot the mics and grid points as 3D scatter plot

fig_grid = plt.figure(1, figsize=(7, 7))
ax = fig_grid.add_subplot(111, projection='3d')
plot_grid1 = ax.scatter(m.mpos[0], m.mpos[1], np.ones(len(m.mpos[2]))*-.5,
                             c='darkorange', marker='o', alpha=1)
plot_grid2 = ax.scatter(scan_xyz[0], scan_xyz[1], scan_xyz[2], c='darkviolet',
                             marker='^', zorder=2)
ax.set_xlabel('$x$ (m)', labelpad=5)
ax.set_ylabel('$y$ (m)', labelpad=5)
ax.set_zlabel('$z$ (m)', labelpad=5)
s = .3
ax.set_xlim(-s, s)
ax.set_ylim(-s, s)
ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)
ax.zaxis.set_tick_params(labelsize=14)
ax.plot(x, y, z, color='black', lw=2, alpha=1, zorder=5)
ax.text(-b-.065, -.1, 0, '%s' % ('$\it{leading}$ $\it{edge}$'), 'y', color='black', zorder=5, fontsize=14)
ax.text(b+.065, -.125, 0, '%s' % ('$\it{trailing}$ $\it{edge}$'), 'y', color='black', zorder=5, fontsize=14)


#ax.quiver(-s, .34, 0, s, 0, 0, color='black', zorder=6, alpha=1, lw=3, arrow_length_ratio=.15, visible=True)
# Create proxy artist to add legend
# --> numpoints = 1 to get only one dot in the legend
# --> linestyle= "none" So there is no line drawn in the legend
scatter1_proxy = mlines.Line2D(
    [0], [0], linestyle="none", c='darkorange', marker='o')
scatter2_proxy = mlines.Line2D([0], [0], linestyle="none", c='darkviolet', marker='^')
ax.legend([scatter1_proxy, scatter2_proxy], ['Triangular array', 'Scanning grid'],
               numpoints=1, fancybox=False, frameon=False, loc='lower center',
               bbox_to_anchor=(0, .925, 1, 0), ncol=2)
ax.view_init(elev=30, azim=-45)
plt.show()
