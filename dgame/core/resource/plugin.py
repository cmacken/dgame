from dgame.core.resource.resource import REGISTER

class ResourcePlugin:

    def __init__(self):

        super().__init__()
        
        print('Compiling resources...')        
        self.RESOURCES = {}

        for resource_obj in REGISTER:
            print(f'     ... adding {resource_obj.shortname}')
            self.RESOURCES[resource_obj.rid] = resource_obj