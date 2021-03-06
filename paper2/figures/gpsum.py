import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from starry_process import StarryProcess
import starry
import os
from tqdm import tqdm

nsamples = 5
norm = Normalize(vmin=0.5, vmax=1.1)
incs = [15, 30, 45, 60, 75, 90]
t = np.linspace(0, 4, 1000)
cmap = plt.get_cmap("plasma_r")
color = lambda i: cmap(0.1 + 0.8 * i / (len(incs) - 1))

map = starry.Map(15, lazy=False)

fig, ax = plt.subplots(
    2,
    nsamples + 1,
    figsize=(12, 2.5),
    gridspec_kw={
        "height_ratios": [1, 0.5],
        "width_ratios": np.append(np.ones(nsamples), 0.1),
    },
)

# Draw samples from a sum of two StarryProcess instances
sp = StarryProcess(
    marginalize_over_inclination=False, r=10, mu=60, sigma=3, c=0.15
)
sp += StarryProcess(
    marginalize_over_inclination=False, r=20, mu=0, sigma=3, n=5, c=0.1
)
y = sp.sample_ylm(nsamples=nsamples).eval()

# Normalize so that the background photosphere
# has unit intensity (for plotting)
y[:, 0] += 1
y *= np.pi

for k in range(nsamples):
    map[:, :] = y[k]
    map.show(ax=ax[0, k], projection="moll", norm=norm)
    ax[0, k].set_ylim(-1.5, 2.25)
    ax[0, k].set_rasterization_zorder(1)
    for i, inc in enumerate(incs):
        map.inc = inc
        flux = map.flux(theta=360.0 * t)
        flux -= np.mean(flux)
        flux *= 1e3
        ax[1, k].plot(t, flux, color=color(i), lw=0.75)

    if k == 0:
        ax[1, k].spines["top"].set_visible(False)
        ax[1, k].spines["right"].set_visible(False)
        ax[1, k].set_xlabel("rotations", fontsize=8)
        ax[1, k].set_ylabel("flux [ppt]", fontsize=8)
        ax[1, k].set_xticks([0, 1, 2, 3, 4])
        for tick in (
            ax[1, k].xaxis.get_major_ticks() + ax[1, k].yaxis.get_major_ticks()
        ):
            tick.label.set_fontsize(6)
        ax[1, k].tick_params(direction="in")
    else:
        ax[1, k].axis("off")

cax = inset_axes(ax[0, -1], width="70%", height="50%", loc="lower center")
cbar = fig.colorbar(ax[0, k].images[0], cax=cax, orientation="vertical")
cbar.set_label("intensity", fontsize=8)
cbar.set_ticks([0.5, 0.75, 1])
cbar.ax.tick_params(labelsize=6)
ax[0, -1].axis("off")

lax = inset_axes(ax[1, -1], width="80%", height="100%", loc="center right")
for i, inc in enumerate(incs):
    lax.plot(0, 0, color=color(i), lw=1, label=r"{}$^\circ$".format(inc))
lax.legend(loc="center left", fontsize=5, frameon=False)
lax.axis("off")
ax[1, -1].axis("off")

dy = max([max(np.abs(ax[1, k].get_ylim())) for k in range(nsamples)])
for k in range(nsamples):
    ax[1, 0].set_ylim(-dy, dy)

# We're done
fig.savefig(
    os.path.abspath(__file__).replace(".py", ".pdf"),
    bbox_inches="tight",
    dpi=300,
)
