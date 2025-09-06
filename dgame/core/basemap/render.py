
    #def render(self) -> np.array:
    #    """
    #    Overlay the greyscaled elevation on the classified RGB array,
    #    embedding the shade effect directly into the RGB values.
    #    """
    #    landclass = self._render_landclass()       # shape: (H, W, 4), dtype=uint8
    #    terrain   = self._render_elevation()      # shape: (H, W), dtype=uint8
    #
    #    strength = self.meta["ELEVATION"]['RENDER_OPACITY']
    #    alpha = int(255 * strength)         # alpha as 0-255
    #
    #    # Extract RGB channels
    #    rgb = landclass[..., :3]
    #
    #    # Blend using integer math: (shade*alpha + rgb*(255-alpha)) / 255
    #    # Use uint16 to prevent overflow, then cast back
    #    blended = ((terrain[..., None].astype(np.uint16) * alpha +
    #                rgb.astype(np.uint16) * (255 - alpha)) // 255).astype(np.uint8)
    #    
    #    return blended
    #
    #
    #def xy_to_latlon(self, x, y):
    #
    #    XMIN = self.meta["INFO"]["X_MIN"]
    #    XMAX = self.meta["INFO"]["X_MAX"]
    #    YMIN = self.meta["INFO"]["Y_MIN"]
    #    YMAX = self.meta["INFO"]["Y_MAX"]
    #
    #    lon = XMIN + (x + 0.5) * (XMAX - XMIN) / self.shape[1] # Width
    #    lat = YMAX - (y + 0.5) * (YMAX - YMIN) / self.shape[0] # Height
 
    #    return (np.clip(lon, a_min=XMIN, a_max=XMAX), # Longitude
    #            np.clip(lat, a_min=YMIN, a_max=YMAX)) # Latitude
 
    #def _render_elevation(self) -> np.ndarray:
    #    """
    #    Take the elevation pixel values, calculate quantile bins, apply to then normalise between 0-255
    #    """
    #    arr = rxr.open_rasterio(self.elev_path).astype(np.uint8)
    #    arr = self.elev.values.squeeze()
 
    #    if arr.dtype != np.uint8:
    #        raise ValueError("Input array must be uint8")
    #    
    #    n_quantiles = self.meta["ELEVATION"]['NQUANT']
 
    #    # Compute quantile edges (0% to 100% split into n_quantiles)
    #    quantiles = np.percentile(arr, np.linspace(0, 100, n_quantiles + 1))
    #    
    #    # Digitize pixels into bins (1..n_quantiles)
    #    bins = np.digitize(arr, quantiles[1:-1], right=True).astype(np.uint8)
    #    
    #    # Scale bins to 0–255
    #    overlay = (bins * (255 // max(1, n_quantiles - 1))).astype(np.uint8)
    #    
    #    return overlay
 
 
    #def _render_landclass(self):
    #    """
    #    Take the classified TIF array then lookup and apply RGB colour for each pixel
    #    """
    #    arr = rxr.open_rasterio(self.ltype_path).astype(np.uint8)
    #    arr = arr.values.squeeze()  # uint8 raster
    #    landtypes = self.LANDTYPES
 
    #    # Build a uint8 lookup table for all possible 0–255 values
    #    lut = np.zeros((256, 3), dtype=np.uint8)
    #    for key, layer in landtypes.items():
    #        lut[key] = layer.COLOUR
 
    #    # Map raster to RGB efficiently (keeps uint8)
    #    rgb = lut[arr]
 
    #    return rgb
 