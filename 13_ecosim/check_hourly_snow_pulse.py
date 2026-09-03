#!/usr/bin/env python3
"""Compare the aligned and late hourly-snow-pulse characterization runs."""

from pathlib import Path
import sys

try:
    import h5py
except ImportError as error:
    raise SystemExit("This checker requires the Python package h5py.") from error


HERE = Path(__file__).resolve().parent
RUNS = {
    "aligned": HERE / "ecosim_hourly_snow_pulse_aligned",
    "late": HERE / "ecosim_hourly_snow_pulse_late",
}
FIELDS = (
    "surface-temperature.cell.0",
    "surface-evaporation_ground.cell.0",
    "surface-snow_depth.cell.0",
)


def require_file(filename):
    if not filename.is_file():
        raise FileNotFoundError(f"required file does not exist: {filename}")


def read_surface_fields(run_directory):
    filename = run_directory / "checkpoint_final.h5"
    require_file(filename)

    values = {}
    with h5py.File(filename, "r") as fid:
        for field in FIELDS:
            if field not in fid:
                raise KeyError(f"dataset {field!r} is missing from {filename}")
            values[field] = float(fid[field][0, 0])
    return values


def main():
    try:
        surface_fields = {
            name: read_surface_fields(directory)
            for name, directory in RUNS.items()
        }
    except (FileNotFoundError, KeyError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    print("Final-time surface fields")
    print(f"  {'field/RUN':42} {'aligned':>20} {'late':>20} {'difference':>20}")
    for field in FIELDS:
        aligned = surface_fields["aligned"][field]
        late = surface_fields["late"][field]
        print(
            f"  {field:42} "
            f"{aligned:20.12g} "
            f"{late:20.12g} "
            f"{late - aligned:20.12g}"
        )

    aligned_snow_depth = surface_fields["aligned"]["surface-snow_depth.cell.0"]
    late_snow_depth = surface_fields["late"]["surface-snow_depth.cell.0"]

    if aligned_snow_depth <= 1.0e-3:
        print(
            "ERROR: aligned run did not accumulate a measurable snowpack",
            file=sys.stderr,
        )
        return 1
    if late_snow_depth >= 0.01 * aligned_snow_depth:
        print(
            "ERROR: late run did not demonstrate the missed snowfall pulse",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
