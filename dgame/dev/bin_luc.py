import rasterio
import numpy as np
from rasterio.windows import Window
from rasterio.enums import Resampling

def reclassify_large_raster(input_path, output_path, reclass_map, tile_size=512):
    """
    Block-wise reclassification of a large int8 raster.
    Saves result as uint8 with legend in colormap (for QGIS).

    Parameters:
    - input_path: str, path to input int8 raster
    - output_path: str, path to output reclassified uint8 raster
    - reclass_map: dict, new_value -> {'values': [...], 'rgb': (r,g,b)}
    - tile_size: int, processing window size
    """
    # Build reverse map: value -> new_value
    flat_map = {}
    colormap = {}
    for new_val, info in reclass_map.items():
        for old_val in info['values']:
            flat_map[old_val] = new_val
        colormap[new_val] = info['rgb']
    colormap[0] = (0, 0, 0)  # 0 reserved as nodata

    with rasterio.open(input_path) as src:
        profile = src.profile
        profile.update(
            dtype='uint8',
            count=1,
            nodata=0,
            compress='deflate'
        )

        with rasterio.open(output_path, 'w', **profile) as dst:
            for y in range(0, src.height, tile_size):
                for x in range(0, src.width, tile_size):
                    window = Window(x, y,
                                    min(tile_size, src.width - x),
                                    min(tile_size, src.height - y))
                    data = src.read(1, window=window)

                    # Initialize output as 0 (nodata)
                    out = np.zeros_like(data, dtype=np.uint8)

                    for old_val, new_val in flat_map.items():
                        out[data == old_val] = new_val

                    dst.write(out, 1, window=window)

            dst.write_colormap(1, colormap)
reclass_map = {
    1: {'values': [1],               'rgb': ( 70, 119, 33)}, # Rainforest
    2: {'values': [2,3,4,5,6,9,10],  'rgb': (101, 132, 56)}, # Forest
    3: {'values': [7, 8, 15],        'rgb': (114, 121, 64)}, # Marshland
    4: {'values': [11,12,13,14],     'rgb': (167, 160, 98)}, # Moorland
    5: {'values': [16,17,18],        'rgb': (131, 173, 78)},    # Plains
    6: {'values': [19],              'rgb': (230, 223, 170)}, # Bare
    7: {'values': [20,23],              'rgb': (166, 206, 227)}, # Water
    8: {'values': [21],              'rgb': (255,255,255)}, # Snow
    9: {'values': [22],              'rgb': (153, 153, 153)}, # URban
}

reclassify_large_raster('D:\\Misc\\Data\\world\\01_RAW\\LANDCOVER.TIF', "aareclassified_out.tif", reclass_map)