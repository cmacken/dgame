import numpy as np
import rasterio
from rasterio.enums import ColorInterp
from rasterio.transform import from_origin
from scipy.ndimage import gaussian_filter
from noise import pnoise2
import random

# Parameters
width, height = 2048, 1024           # Output size
seed = 12                           # Random seed for reproducibility
scale = 0.45                    # Noise scale
octaves = 6
persistence = 0.4
lacunarity = 3.0
terrain_bins = [0.2, 0.4, 0.6, 0.8]  # Elevation thresholds for terrain classes
land_classes = {
    0: ("Water", (30, 60, 180)),
    1: ("Grassland", (90, 200, 90)),
    2: ("Forest", (20, 120, 40)),
    3: ("Desert", (220, 200, 90)),
    4: ("Mountain", (150, 150, 150)),
    5: ("Tundra", (180, 220, 220))
}

np.random.seed(seed)
random.seed(seed)

# --- Generate base noise field ---
noise_field = np.zeros((height, width), dtype=np.float32)
for y in range(height):
    for x in range(width):
        nx, ny = x / width - 0.5, y / height - 0.5
        noise_field[y, x] = pnoise2(nx / scale, ny / scale, octaves, persistence, lacunarity, repeatx=1024, repeaty=1024, base=seed)

# Smooth and normalize
noise_field = gaussian_filter(noise_field, sigma=3)
noise_field = (noise_field - noise_field.min()) / (noise_field.max() - noise_field.min())

# --- Create land/water mask ---
sea_level = 0.45
is_land = noise_field > sea_level

# --- Generate terrain bins (0 = water, then binned land) ---
terrain = np.zeros_like(noise_field, dtype=np.uint8)
if is_land.any():
    land_elev = (noise_field - sea_level) / (1 - sea_level)
    for i, t in enumerate(terrain_bins, start=1):
        terrain[(land_elev >= (t - 0.2)) & (land_elev < t)] = i
    terrain[land_elev >= terrain_bins[-1]] = len(terrain_bins)
terrain[~is_land] = 0

# --- Generate land type raster (categorical) ---
landtype = np.zeros_like(terrain, dtype=np.uint8)
landtype[~is_land] = 0  # water

# Assign random land classes to continents
# Use different thresholds to simulate variety
for mask_val, (name, _) in list(land_classes.items())[1:]:
    mask = (is_land) & (np.random.random((height, width)) > 0.8)
    landtype[mask] = mask_val

# Blend based on elevation to give some structure
landtype[(terrain == len(terrain_bins)) & is_land] = 4  # high = mountain
landtype[(terrain == 1) & is_land] = 1                  # lowland = grassland
landtype[(terrain == 2) & is_land] = 2                  # midland = forest
landtype[(terrain == 3) & is_land] = 3                  # arid
landtype[(terrain == 4) & is_land] = 5                  # cold = tundra

# --- Define color map (palette) ---
colormap = {idx: rgb for idx, (_, rgb) in land_classes.items()}

# --- Write GeoTIFFs ---
transform = from_origin(-180, 90, 0.5, 0.5)  # arbitrary geotransform
profile = {
    'driver': 'GTiff',
    'dtype': rasterio.uint8,
    'width': width,
    'height': height,
    'count': 1,
    'crs': 'EPSG:4326',
    'transform': transform
}

# Landtype with color map
with rasterio.open('landtype.tif', 'w', **profile) as dst:
    dst.write(landtype, 1)
    dst.write_colormap(1, colormap)
    dst.colorinterp = [ColorInterp.palette]
print("✅ landtype.tif written with color map.")

# Terrain (no color map)
with rasterio.open('terrain.tif', 'w', **profile) as dst:
    dst.write(terrain, 1)
print("✅ terrain.tif written.")

import matplotlib.pyplot as plt
rgb = np.stack([np.vectorize(lambda v: colormap[v][i])(landtype) for i in range(3)], axis=-1).astype(np.uint8)
plt.imshow(rgb)
plt.axis('off')
plt.show()