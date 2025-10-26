#!/usr/bin/env python3
"""
Fix raster CRS and extent to EPSG:4326 (-180 to 180, -90 to 90)
and save as uint8.
"""

import sys
import numpy as np
import rioxarray
from pathlib import Path


def fix_raster(in_path: str):
    in_path = Path(in_path)
    out_path = in_path.with_name(f"{in_path.stem}_fixed{in_path.suffix}")

    print(f"Loading {in_path} ...")
    da = rioxarray.open_rasterio(in_path, masked=True).squeeze()

    # --- Set or correct CRS ---
    if da.rio.crs is None:
        print("No CRS found — assuming EPSG:4326.")
        da = da.rio.write_crs("EPSG:4326", inplace=False)
    elif da.rio.crs.to_epsg() != 4326:
        print(f"Reprojecting from {da.rio.crs} to EPSG:4326 ...")
        da = da.rio.reproject("EPSG:4326")

    # --- Reset extent to world bounds ---
    ny, nx = da.sizes["y"], da.sizes["x"]
    da = da.assign_coords({
        "x": np.linspace(-180, 180, nx),
        "y": np.linspace(90, -90, ny),  # descending y for north-down
    })

    # --- Convert to uint8 ---
    if da.dtype != np.uint8:
        print(f"Converting data from {da.dtype} → uint8 ...")
        da = da.astype(np.uint8)

    # --- Write output ---
    print(f"Saving corrected raster to {out_path}")
    da.rio.to_raster(out_path, dtype="uint8")

    print("✅ Done.")
    return out_path


if __name__ == "__main__":

    fix_raster(sys.argv[1])