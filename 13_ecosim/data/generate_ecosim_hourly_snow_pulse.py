#!/usr/bin/env python3
"""Generate the synthetic hourly meteorological forcing used by EcoSIM tests."""

from pathlib import Path

import h5py
import numpy as np


output = Path(__file__).with_name("ecosim_hourly_snow_pulse.h5")
time = np.array([0.0, 3600.0, 7200.0])

forcing = {
    "time [s]": time,
    # A rate of 1.e-6 m/s gives 3.6 mm SWE over the first hour.
    "precipitation snow [m SWE s^-1]": np.array([1.0e-6, 0.0, 0.0]),
    "precipitation rain [m s^-1]": np.zeros_like(time),
    "air temperature [K]": np.full_like(time, 268.15),
    "incoming shortwave radiation [W m^-2]": np.zeros_like(time),
    "vapor pressure air [Pa]": np.full_like(time, 400.0),
    "wind speed [m s^-1]": np.full_like(time, 1.0),
}

with h5py.File(output, "w") as fid:
    for name, values in forcing.items():
        fid.create_dataset(name, data=values)

print(output)
