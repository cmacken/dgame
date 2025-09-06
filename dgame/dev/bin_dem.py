import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window
import os

def bin_dem_to_uint8(input_path: str, output_path: str):
    """
    Reads an int16 DEM from file, bins it into 100 m intervals capped at -300 m,
    and writes the result as a uint8 raster with 1-based bin labels.

    Parameters:
        input_path (str): Path to the input DEM (GeoTIFF).
        output_path (str): Path to the output binned raster (GeoTIFF).
    """
    with rasterio.open(input_path) as src:
        profile = src.profile.copy()
        profile.update(dtype=rasterio.uint8, count=1, compress='lzw')

        with rasterio.open(output_path, 'w', **profile) as dst:
            for ji, window in src.block_windows(1):
                data = src.read(1, window=window)

                # Handle NoData if present
                if src.nodata is not None:
                    mask = data == src.nodata
                else:
                    mask = np.full(data.shape, False, dtype=bool)

                # Cap at -300 m
                capped = np.maximum(data, -300)

                # Bin to 100 m intervals, offset by +300, then label from 1
                bins = ((capped + 300) // 100 + 1).astype(np.uint8)

                # Restore NoData mask to 0
                bins[mask] = 0

                dst.write(bins, window=window, indexes=1)
# Example usage
if __name__ == "__main__":
    bin_dem_to_uint8(
        input_path="D:\\Misc\\Data\\world\\01_RAW\\TERRAIN.TIF",
        output_path="out.tif",
    )
