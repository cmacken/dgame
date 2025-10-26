import json
from importlib.resources import files
from pathlib import Path
import rasterio
from dgame.core.logger import get_logger

logger = get_logger(__name__)

def load_json(path):
    logger.info(f'Loading JSON : {path}')
    with open(path) as f:
        data = json.load(f)
    return data

def get_package_path(args):
    out = files("dgame").joinpath(*args)    
    logger.info(f'Resolved {args} -> : {out}')
    return out

def read_tif(path):
    """
    Read a GeoTIFF file into a NumPy array with metadata.
    
    Returns
    -------
    data : np.ndarray
        The raster data as a NumPy array. Shape: (bands, height, width)
    profile : dict
        Raster metadata including CRS, transform, dtype, etc.
    """
    logger.debug(f'Reading TIF : {path}')
    with rasterio.open(path) as src:
        data = src.read()  # All bands -> shape (bands, height, width)
        profile = src.profile
    return data, profile
