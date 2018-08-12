import esper
import component
import pygame
import sys

class GravityProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for oEntity, (oVelocity, oGravity) in self.world.get_components(component.Velocity, component.Gravity):
            oVelocity.y = oVelocity.y + oGravity.iForce
