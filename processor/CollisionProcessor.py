import esper
import component
import pygame

class CollisionProcessor(esper.Processor):
    def __init__(self, oScreen):
        super().__init__()

    def process(self):
        self.collisionMap()

    def collisionMap(self):
    	pass
