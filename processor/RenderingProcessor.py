import esper
import component
import pygame
import Constant

class RenderingProcessor(esper.Processor):
    def __init__(self, oScreen):
        super().__init__()
        self.oScreen = oScreen

    def process(self):
        self.oScreen.fill( (0,0,0) )
        self.renderMap()

        for oEntity, (oPosition, oSize) in self.world.get_components(component.Position, component.Size):
            oRect = pygame.Rect(oPosition.x, oPosition.y, oSize.fWidth, oSize.fHeight)
            pygame.draw.rect(self.oScreen, (255, 0, 255), oRect)

        pygame.display.flip()

    # Find the entity with the component Map
    # Enumerate the matrice to find each value at a position (x,y)
    # Render with the correct image associate in aRender for each value
    def renderMap(self):
        for oEntity, (oMap) in self.world.get_component(component.Map):
            for y, aX in enumerate(oMap.aMap):
                for x, iValue in enumerate(aX):
                    oRect = pygame.Rect(x * Constant.CELL_WIDTH, y * Constant.CELL_HEIGHT , Constant.CELL_WIDTH, Constant.CELL_HEIGHT)
                    pygame.draw.rect(self.oScreen, oMap.aRender.get(iValue, (255,255,255)), oRect)
