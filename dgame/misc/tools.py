import json
from importlib.resources import files
from pathlib import Path


def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def get_colourmap(layer):

    visual_params = layer.VISUALISE
    array = layer.data


    if visual_params['TYPE'] == 'QUANTILE':

        colourmap_name = visual_params['COLOURMAP']
        n_quantiles = visual_params['NQUANT']
        ignore_values = visual_params['IGNORE']

    if visual_params['TYPE'] == 'LINEAR':

        ignore_values = visual_params['IGNORE']


def get_asset_path(*args):
    return files("dgame.assets").joinpath(*args)

