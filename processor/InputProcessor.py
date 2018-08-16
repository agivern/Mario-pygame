import esper
import component
import pygame
import sys

class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.pressed_K_a = False
        self.pressed_K_d = False

    def process(self):
        for oEntity, (oPlayer, oVelocity) in self.world.get_components(component.Player, component.Velocity):

            for event in pygame.event.get():
                # Si la croix de la fenetre est declenche, on stop le jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                # Si une touche est presse
                elif event.type == pygame.KEYDOWN:
                    # Touche Q, on rajoute une velocity vers la gauche a l'objet player
                    if event.key == pygame.K_a:
                        self.pressed_K_a = True

                    # Touche D, on rajoute une velocity vers la droite a l'objet player
                    if event.key == pygame.K_d:
                        self.pressed_K_d = True

                    # Touche Z, on rajoute une velocity vers le haut a l'objet player
                    # Si le player va deja vers le haut, on empeche le double saut
                    if event.key == pygame.K_SPACE and oVelocity.y == 0:
                        oVelocity.y = -15
                    # Touche ECHAP, on stop le jeu
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.pressed_K_a = False
                    # Touche D, on rajoute une velocity vers la droite a l'objet player
                    if event.key == pygame.K_d:
                        self.pressed_K_d = False

            if self.pressed_K_a:
                oVelocity.x -= 4
            if self.pressed_K_d:
                oVelocity.x += 4

            break
