# core/entities.py
from uuid import uuid4

class Entity:
    
    def __init__(self):
        self.id = str(uuid4())
        self.components = {}
        self.hide = False

    def add(self, component):
        self.components[type(component)] = component
        component.entity = self

    def get(self, component_type):
        return self.components.get(component_type)

    def has(self, *component_types):
        return all(t in self.components for t in component_types)