import esper
import component
import pygame
import Constant

class CollisionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for oEntity, (oPosition, oVelocity, oSize) in self.world.get_components(component.Position, component.Velocity, component.Size):
            self.collisionMap(oPosition, oVelocity, oSize)

    def collisionMap(self, oPosition, oVelocity, oSize):
        for oEntity, (oMap) in self.world.get_component(component.Map):
            iMapX = int(oPosition.x) // Constant.CELL_WIDTH
            iMapY = int(oPosition.y + oVelocity.y) // Constant.CELL_HEIGHT

            iLength = int(oSize.fWidth) // Constant.CELL_WIDTH
            iHeight = int(oSize.fHeight) // Constant.CELL_HEIGHT

            if oVelocity.y >= 0:
                iMapY = iMapY + iHeight

            for i in (0, iLength, 1):
                if oMap.aMap[iMapY][iMapX + i] == 1:
                    oVelocity.y = 0

            if oVelocity.x != 0:
                iMapX = int(oPosition.x) // Constant.CELL_WIDTH
                iMapY = int(oPosition.y + oVelocity.y) // Constant.CELL_HEIGHT

                if oVelocity.x > 0 :
                    iMapX = iMapX + iLength

                for i in (0, iHeight, 1):
                    if oMap.aMap[iMapY + i ][iMapX] == 1:
                        oVelocity.x = 0
