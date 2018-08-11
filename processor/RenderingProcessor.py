import esper
import component
import pygame

class RenderingProcessor(esper.Processor):
    def __init__(self, oScreen):
        super().__init__()
        self.oScreen = oScreen

    def process(self):
        self.oScreen.fill( (0,0,0) )
        for oEntity, (oPosition, oSize) in self.world.get_components(component.Position, component.Size):
            oRect = pygame.Rect(oPosition.x, oPosition.y, oSize.iWidth, oSize.iHeight)
            pygame.draw.rect(self.oScreen, (255, 0, 255), oRect)

        pygame.display.flip()
