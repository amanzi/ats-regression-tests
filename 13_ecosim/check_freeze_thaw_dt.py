#!/usr/bin/env python3
"""Check the 3599 s and 3600 s EcoSIM timestep characterization runs."""

from pathlib import Path
import sys

try:
    import h5py
except ImportError as error:
    raise SystemExit("This checker requires the Python package h5py.") from error


HERE = Path(__file__).resolve().parent
RUNS = {
    "3600 s": HERE / "ecosim_freeze_thaw_dt_3600s",
    "3599 s": HERE / "ecosim_freeze_thaw_dt_3599s",
}
EXPECTED_ADVANCES = {
    "3600 s": 24,
    "3599 s": 12,
}
FIELDS = (
    "surface-temperature.cell.0",
    "surface-evaporation_ground.cell.0",
    "surface-snow_depth.cell.0",
)


def require_file(filename):
    if not filename.is_file():
        raise FileNotFoundError(f"required file does not exist: {filename}")


def count_ecosim_advances(run_directory):
    logfile = run_directory / "log"
    if not logfile.is_file():
        print(
            f"log of screen output in file `log` not available for "
            f"{run_directory}"
        )
        return None
    return logfile.read_text(errors="replace").count("Running EcoSIM Advance")


def read_surface_fields(run_directory):
    checkpoint = run_directory / "checkpoint_final.h5"
    require_file(checkpoint)

    values = {}
    with h5py.File(checkpoint, "r") as fid:
        for field in FIELDS:
            if field not in fid:
                raise KeyError(f"dataset {field!r} is missing from {checkpoint}")
            values[field] = float(fid[field][0, 0])
    return values


def main():
    try:
        advances = {
            name: count_ecosim_advances(directory)
            for name, directory in RUNS.items()
        }
        surface_fields = {
            name: read_surface_fields(directory)
            for name, directory in RUNS.items()
        }
    except (FileNotFoundError, KeyError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    print("EcoSIM advance counts")
    for name in ("3600 s", "3599 s"):
        if advances[name] is not None:
            print(
                f"  {name}: {advances[name]} "
                f"(expected {EXPECTED_ADVANCES[name]})"
            )

    print("\nFinal surface fields")
    print(f"  {'field/RUN':42} {'dt=3600 s':>20} {'dt=3599 s':>20} {'difference':>20}")
    for field in FIELDS:
        value_3600 = surface_fields["3600 s"][field]
        value_3599 = surface_fields["3599 s"][field]
        print(
            f"  {field:42} "
            f"{value_3600:20.12g} "
            f"{value_3599:20.12g} "
            f"{value_3599 - value_3600:20.12g}"
        )

    wrong_counts = [
        name
        for name, expected in EXPECTED_ADVANCES.items()
        if advances[name] is not None and advances[name] != expected
    ]
    if wrong_counts:
        for name in wrong_counts:
            print(
                f"ERROR: {name} run had {advances[name]} EcoSIM advances; "
                f"expected {EXPECTED_ADVANCES[name]}",
                file=sys.stderr,
            )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
