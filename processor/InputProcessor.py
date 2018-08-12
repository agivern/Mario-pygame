import esper
import component
import pygame
import sys

class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for event in pygame.event.get():
            # Si la croix de la fenetre est declenche, on stop le jeu
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # Si une touche est presse
            elif event.type == pygame.KEYDOWN:
                for oEntity, (oPlayer, oVelocity) in self.world.get_components(component.Player, component.Velocity):
                    # Touche Q, on rajoute une velocity vers la gauche a l'objet player
                    if event.key == pygame.K_a:
                        oVelocity.x = -2
                    # Touche D, on rajoute une velocity vers la droite a l'objet player
                    if event.key == pygame.K_d:
                        oVelocity.x = 2
                    # Touche Z, on rajoute une velocity vers le haut a l'objet player
                    # Si le player va deja vers le haut, on empeche le double saut
                    if event.key == pygame.K_z and oVelocity.y == 0:
                        oVelocity.y = -10
                    # Touche ECHAP, on stop le jeu
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
