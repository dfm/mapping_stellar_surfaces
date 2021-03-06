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
calibrate.run_batch(
    path=abspath("data/batch_default_1000"),
    generate=dict(nlc=1000),
    sample=dict(compute_inclination_pdf=False),
    plot_data=False,
    plot_corner_transformed=False,
    plot_latitude_pdf=False,
    plot_inclination_pdf=False,
)

# Copy output to this directory
copy(
    "batch_default_1000",
    "calibration_corner.png",
    "calibration_batch_default_1000_corner.png",
)
