from starry_process import calibrate
import numpy as np
import os
import shutil

# Utility funcs to move figures to this directory
abspath = lambda *args: os.path.join(
    os.path.dirname(os.path.abspath(__file__)), *args
)
copy = lambda name, src, dest: shutil.copyfile(
    abspath("data", name, src), abspath(dest)
)

# Run
calibrate.run(
    path=abspath("data/midlat"),
    generate=dict(latitude=dict(mu=45)),
    plot_data=False,
    plot_inclination_pdf=False,
)

# Copy output to this directory
copy("midlat", "corner_transformed.pdf", "calibration_midlat_corner.pdf")
copy("midlat", "latitude.pdf", "calibration_midlat_latitude.pdf")
