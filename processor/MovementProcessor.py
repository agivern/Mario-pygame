import esper
import component

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for oEntity, (oVelocity, oPosition) in self.world.get_components(component.Velocity, component.Position):
            oPosition.x += oVelocity.x
            oPosition.y += oVelocity.y

            oVelocity.x = 0
            oVelocity.y = 0
