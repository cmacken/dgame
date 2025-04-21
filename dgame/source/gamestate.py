


class GameState:

    def __init__(self):

        self.t = 0.0
        self.entities = []


    def update(self):
        print('refreshing entities')
        pass


    def _create_new_id(self):
        unique_ids = set([i.id for i in self.entities])
        max_id = max(unique_ids)
        return max_id + 1


    def add_entity(self, obj):

        new_id = self._create_new_id()
        obj.set_id(new_id)
        self.entities.append(obj)


    def del_entity(self, obj_id):

        self.entities = [obj for obj in self.entities if obj.id != obj_id]


    