import numpy as np
import xarray as xr
import rioxarray
import geopandas as gpd
from shapely.geometry import Point, box

from dgame.core.utils import get_package_path, load_json, get_logger
from dgame.core.component import Resource, Terrain, Condition  # assume these exist

logger = get_logger(__name__)


# --------------------------
# --- Base Layer Classes ---
# --------------------------

class MapLayer:
    def __init__(self, name, metadata=None):
        self.name = name
        self.metadata = metadata or {}

    def query(self, x: float, y: float, tick: int = 0):
        raise NotImplementedError


class RasterLayer(MapLayer):
    def __init__(self, name: str, data: xr.DataArray, metadata=None):
        logger.info(f"Creating raster layer: {name}")
        super().__init__(name, metadata)
        self.data = data
        if self.data.rio.crs is None:
            self.data = self.data.rio.write_crs("EPSG:4326", inplace=False)

    def query(self, lon: float, lat: float, tick: int = 0):
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            logger.warning(f"Query point ({lon},{lat}) outside global bounds.")
            return np.nan
        return float(self.data.interp(x=lon, y=lat, method="nearest").values)


class VectorLayer(MapLayer):
    def __init__(self, name: str, gdf: gpd.GeoDataFrame, provides: list[str], field: str, metadata=None):
        logger.info(f"Creating vector layer: {name}")
        super().__init__(name, metadata)
        self.gdf = gdf
        self.provides = provides
        self.field = field

        if self.gdf.crs is None:
            logger.warning(f"Vector layer {name} had no CRS; assuming EPSG:4326.")
            self.gdf = self.gdf.set_crs("EPSG:4326")
        elif self.gdf.crs.to_epsg() != 4326:
            logger.info(f"Reprojecting vector layer {name} to EPSG:4326.")
            self.gdf = self.gdf.to_crs("EPSG:4326")

    def query(self, lon: float, lat: float, tick: int = 0):
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            return {rid: 0.0 for rid in self.provides}

        pt = Point(lon, lat)
        matches = self.gdf[self.gdf.intersects(pt)]

        if matches.empty:
            return {rid: 0.0 for rid in self.provides}

        total_value = float(matches[self.field].sum())
        return {rid: total_value for rid in self.provides}


# --------------------------
# --- Map Class ------------
# --------------------------

class Map:
    def __init__(self):
        logger.info(f"Initializing Map...")
        self.config = load_json(get_package_path(["map", "map_config.json"]))

        self.layers = {}
        self.context_layers = {}
        self.resources = {}
        self.conditions = {}
        self.terrains = {}

        # --- Base layers ---
        self._load_base_layers()

        # --- Definitions ---
        self._setup_terrains()
        self._setup_resources()
        self._setup_conditions()

        # --- Layers ---
        self._setup_resource_layers()
        self._setup_condition_layers()

    # -----------------------
    # --- Base layer setup ---
    # -----------------------

    def _load_base_layers(self):
        base_cfg = self.config["base"]
        terrain = rioxarray.open_rasterio(get_package_path(base_cfg["terrain_path"]), masked=True).squeeze().astype('uint8')
        elevation = rioxarray.open_rasterio(get_package_path(base_cfg["elevation_path"]), masked=True).squeeze().astype('uint8')

        if terrain.shape != elevation.shape:
            raise ValueError("Terrain and elevation must match in shape")

        self.layers["terrain"] = RasterLayer("terrain", terrain, {"units": ""})
        self.layers["elevation"] = RasterLayer("elevation", elevation, {"units": "m"})

    # -----------------------
    # --- Definitions setup ---
    # -----------------------

    def _setup_terrains(self):
        logger.info("Registering terrains...")
        for ter in self.config["terrains"]:
            dn = ter["dn"]
            self.terrains[dn] = Terrain(
                dn=dn,
                name=ter["name"],
                rgb=tuple(ter["rgb"]),
                desc=ter["desc"]
            )
        logger.info(f"Loaded {len(self.terrains)} terrains.")

    def _setup_resources(self):
        logger.info("Registering resources...")
        for res in self.config["resources"]["defs"]:
            rid = res["rid"]
            self.resources[rid] = Resource(
                rid=rid,
                name=res["name"],
                units=res["units"],
                offset=res["offset"],
                scale=res["scale"]
            )
        logger.info(f"Loaded {len(self.resources)} resources.")

    def _setup_conditions(self):
        logger.info("Registering conditions...")
        for cond in self.config["conditions"]["defs"]:
            cid = cond["cid"]
            self.conditions[cid] = Condition(
                cid=cid,
                name=cond["name"],
                units=cond["units"],
                offset=cond["offset"],
                scale=cond["scale"]
            )
        logger.info(f"Loaded {len(self.conditions)} conditions.")

    # -----------------------
    # --- Layers setup ---
    # -----------------------

    def _setup_resource_layers(self):
        for layer_cfg in self.config["resources"]["layers"]:
            name = layer_cfg["name"]
            gdf = gpd.read_file(get_package_path(layer_cfg["path"]))
            gdf = gdf.to_crs("EPSG:4326").clip(box(-180, -90, 180, 90))

            layer = VectorLayer(
                name=name,
                gdf=gdf,
                provides=layer_cfg["provides"],
                field=layer_cfg["field"]
            )
            self.context_layers[name] = layer
            logger.info(f"Loaded resource layer '{name}'")

    def _setup_condition_layers(self):
        for layer_cfg in self.config["conditions"]["layers"]:
            name = layer_cfg["name"]
            da = rioxarray.open_rasterio(get_package_path(layer_cfg["path"]), masked=True).squeeze()
            da = da.rio.write_crs("EPSG:4326", inplace=False)
            da = da.assign_coords({
                "x": np.linspace(-180, 180, da.sizes["x"]),
                "y": np.linspace(90, -90, da.sizes["y"]),
            }).astype("uint8")

            layer = RasterLayer(name, da, {"cid": layer_cfg["cid"]})
            self.context_layers[name] = layer
            logger.info(f"Loaded condition layer '{name}'")

    # -----------------------
    # --- Querying ---
    # -----------------------

    def query(self, x: float, y: float, tick: int = 0):
        result = {
            "terrain": None,
            "elevation": None,
            "resources": {},
            "conditions": {}
        }

        try:
            tkey = self.layers["terrain"].query(x, y, tick)
            result["terrain"] = self.terrains.get(int(tkey))
        except Exception as e:
            logger.warning(f"Terrain query failed: {e}")
            result["terrain"] = np.nan

        try:
            result["elevation"] = self.layers["elevation"].query(x, y, tick)
        except Exception as e:
            logger.warning(f"Elevation query failed: {e}")
            result["elevation"] = np.nan

        for name, layer in self.context_layers.items():
            try:
                value = layer.query(x, y, tick)
            except Exception as e:
                logger.warning(f"Layer '{name}' query failed: {e}")
                continue

            if isinstance(layer, VectorLayer):
                for rid, val in value.items():
                    resource_obj = self.resources.get(rid)
                    if resource_obj:
                        result["resources"][resource_obj] = result["resources"].get(resource_obj, 0.0) + val
            elif isinstance(layer, RasterLayer):
                cid = layer.metadata.get("cid")
                condition_obj = self.conditions.get(cid)
                if condition_obj:
                    result["conditions"][condition_obj] = value

        logger.info(result)
        return result
