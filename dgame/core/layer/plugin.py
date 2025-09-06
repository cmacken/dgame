from dgame.core.layer.layer import REGISTER

class LayerPlugin:
    """Stores layers and allows access by SHORTNAME or NAME."""

    def __init__(self):

        print('Compiling layers...')
        self.LAYERS = {}
        for layer_obj in REGISTER:
            print(f'     ... adding {layer_obj.shortname}')
            self.LAYERS[layer_obj.lid] = layer_obj