import rasterio
from rasterio.enums import Resampling
from rasterio.shutil import copy as rio_copy
from rasterio.transform import Affine

def convert_to_cog(input_path: str, output_path: str, blocksize: int = 512):
    """
    Converts a GeoTIFF to a Cloud-Optimized GeoTIFF (COG) with tiling, overviews, and compression.

    Parameters:
        input_path (str): Path to the input GeoTIFF.
        output_path (str): Path to save the COG.
        blocksize (int): Tile size (default 512x512). Must be a power of 2.
    """
    # First, open the input file
    with rasterio.open(input_path) as src:
        profile = src.profile.copy()

        # Update profile for COG
        profile.update({
            'driver': 'GTiff',
            'tiled': True,
            'blockxsize': blocksize,
            'blockysize': blocksize,
            'compress': 'deflate',
            'interleave': 'pixel',
            'BIGTIFF': 'IF_SAFER'
        })

        # Build overviews before writing to COG
        overviews = [2, 4, 8, 16, 32]
        overview_resampling = Resampling.average if src.count == 1 else Resampling.nearest

        with rasterio.open('/vsimem/temp.tif', 'w', **profile) as tmp_dst:
            tmp_dst.write(src.read())
            tmp_dst.build_overviews(overviews, overview_resampling)
            tmp_dst.update_tags(ns='rio_overview', resampling=overview_resampling.value)

        # Final copy to COG-compliant file
        rio_copy('/vsimem/temp.tif', output_path, copy_src_overviews=True, **profile)



convert_to_cog("D:\\Misc\\Data\\world\\REDUX\\FINAL\\TERRAIN-FINAL.tif",
               "TERRAIN-FINAL-COG.tif")