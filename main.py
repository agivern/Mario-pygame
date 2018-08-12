import pygame
import sys
import esper
import processor
import component

# Variables statiques du jeu
FPS = 60 # Nombre de cycle du jeu par seconde
RESOLUTION = (600, 400) # Resolution de la fenetre de jeu
CELL_WIDTH = 32 # Longueur d'une case du jeu
CELL_HEIGHT = 32 # Hauteur d'une case du jeu

# Variables globales du jeu
aEntities = list()

################################################################################
# Entity permet de creer des objets qui s affichent et qui sont mis a jour a chaque cycle de notre jeu
# Les collisions sont egalement gere lors d'un deplacement d'une entite
# Une entite est compose d'une posistion, une taille, une direction et une image/couleur
class Entity:
    # Initialisation d'une entite, sa position initiale doit etre defini
    # Possibilite de retirer l'effet de la gravite sur l'entite (pour les objets volant par exemple)
    def __init__(self, fPositionX, fPositionY, bGravity = True):
        self.fPositionX = fPositionX
        self.fPositionY = fPositionY
        self.fWidth = 32
        self.fHeight = 32
        self.color = (255, 0, 255)
        self.fVelocityX = 0.0
        self.fVelocityY = 1.0
        self.bGravity = bGravity


    # Affichage de l'image de l'entite a sa position sur l'ecran
    def render(self, oScreen):
        oRect = pygame.Rect(self.fPositionX, self.fPositionY, self.fWidth, self.fHeight)
        pygame.draw.rect(oScreen, self.color, oRect)

    # Fonction vide, modifiable lors d'un heritage pour gerer les collisions avec les autres entites
    def _collideEntity  (self, oEntity):
        pass

    # Fonction pour gerer la collision d'une entite lors d'un deplacement avec la carte
    def _colisionMap(self, aMap):
        # Deplacement vertical
        # Position de la map en collision
        iPositionMapX = int(self.fPositionX) // CELL_WIDTH
        iPositionMapY = int(self.fPositionY + self.fVelocityY) // CELL_HEIGHT

        # Si l'entite tombe, on regarde la map en dessous de lui
        if self.fVelocityY >= 0:
            iPositionMapY = iPositionMapY + 1

        # Si la map contient un mur, la vitesse sur l'axe vertical est mis a 0
        if aMap[iPositionMapY][iPositionMapX] == 1:
            self.fVelocityY = 0
        # Verification de collision sur le bloc a cote lorsque l'entite est sur deux blocs de la map
        elif (iPositionMapX + 1) < len(aMap[iPositionMapY]) and self.fPositionX % CELL_WIDTH > 0 and aMap[iPositionMapY][iPositionMapX + 1] == 1:
            self.fVelocityY = 0

        # Deplacement horizontal
        if self.fVelocityX != 0:
            # Position de la map en collision
            iPositionMapY = int(self.fPositionY) // CELL_HEIGHT
            iPositionMapX = int(self.fPositionX + self.fVelocityX) // CELL_WIDTH

            # Si l'entite va vers la droite, on regarde la map a sa droite
            if self.fVelocityX > 0 :
                iPositionMapX = iPositionMapX + 1

            # Si la map contient un mur, la vitesse sur l'axe horizontal est mis a 0
            if aMap[iPositionMapY][iPositionMapX] == 1:
                self.fVelocityX = 0
            # Verification de collision sur le bloc a cote lorsque l'entite touche deux blocs de la map
            elif iPositionMapY + 1 < len(aMap) and self.fPositionY % CELL_HEIGHT > 0 and aMap[iPositionMapY + 1][iPositionMapX] == 1 :
                self.fVelocityX = 0

    # Fonction pour verfier et declencher la gestion de collision entre l'entite et les autres entite de la map
    def _collideEntities(self):
        aEntitiesRect = list()
        aOtherEntities = list()

        # On parcoure toutes les entites sur la map
        for oEntity in aEntities:
            # On ne recupere que les entites qui ne correspondent pas a l'instance
            if self is not oEntity:
                # On stock un rectangle a la position de chaque entites.
                # Afin de conserver un ensemble d'index similaire, on stock les entites dans le meme ordre
                # dans une seconde liste
                oRect = pygame.Rect(oEntity.fPositionX, oEntity.fPositionY, oEntity.fWidth, oEntity.fHeight)
                aEntitiesRect.append(oRect)
                aOtherEntities.append(oEntity)

        # On regarder avec quels indexs notre instance rentre en collision
        oRect = pygame.Rect(self.fPositionX, self.fPositionY, self.fWidth, self.fHeight)
        aIndexCollide = oRect.collidelistall(aEntitiesRect)
        # Si il y a au moins une collision, on declenche un event de collision avec l'entite
        if len(aIndexCollide) > 0:
            for iIndex in aIndexCollide:
                self._collideEntity(aOtherEntities[iIndex])

    # Mise a jour de l'entite
    # On verifie sa collision avec la map, ensuite on deplace l'entite si besoin
    # Puis on verifie sa collision avec les autres entites
    def update(self, aMap):
        # Verification des collisions, cela met a jour la velocity pour stopper le deplacement
        self._colisionMap(aMap)

        # On deplace l'entite de facon horizontal a la vitesse de sa velocity
        self.fPositionX += self.fVelocityX

        # On deplace l'entite vers le haut ou le bas de 2 si il y a une velocity sur l'axe vertical
        if self.fVelocityY > 0 and self.bGravity:
            self.fPositionY += 2
        elif self.fVelocityY < 0 and self.bGravity:
            self.fPositionY -= 2

        # On met a jour la velocity (on cree un ralentissement pour creer un effet de glissade)
        if self.fVelocityX != 0:
            tmpVelocityX = self.fVelocityX
            self.fVelocityX = self.fVelocityX - (0.2)
            # Remise a 0 de la vitesse pour ne pas faire un deplacement oppose a la direction
            if abs(tmpVelocityX) <= abs(self.fVelocityX):
                self.fVelocityX = 0

        # On met a jour la velocity sur l'axe vertical en forcant la chute
        if self.fVelocityY < 1:
            self.fVelocityY += 0.2
            # On bloque la velocity de chute a 1
            if self.fVelocityY > 1:
                self.fVelocityY = 1.0

        # Test des collisions avec les autres entites
        self._collideEntities()


################################################################################

# Class qui herite de Entity
# Permet de rajouter la collision entre le player et la victoire et d'avoir un affichage de victoire
class Player(Entity):
    def __init__(self, fPositionX, fPositionY, bGravity = True):
        Entity.__init__(self, fPositionX, fPositionY, bGravity)
        self.color = (255,0,0)
        # Nouvelle variable pour gerer l'etat de victoire
        self.bVictory = False

    def _collideEntity(self, oEntity):
        # Si l'entite en collision est une instance de Victory, on change l'etat de bVictory a True
        if isinstance(oEntity, Victory):
            self.bVictory = True

    def render(self, oScreen):
        Entity.render(self, oScreen)
        # Si l'etat de victoire est a True, on affiche Victoire sur l'ecran
        if self.bVictory:
            myfont = pygame.font.SysFont('monospace', 15)
            label = myfont.render("Victoire !", 1, (0, 0, 0))
            oScreen.blit(label, (100, 100))

################################################################################

# Class qui herite de Entity
# Permet d'avoir des instances de Victory pour gerer la victoire en cas de collision avec ceux-ci
class Victory(Entity):
    def __init__(self, fPositionX, fPositionY, bGravity = True):
        Entity.__init__(self, fPositionX, fPositionY, bGravity)
        self.color = (255, 255, 0)

# Fonction principal qui fait tourner le jeu
def run():
    pygame.init()
    oScreen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption('mario')
    oClock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    oWorld = esper.World()

    oWorld.add_processor(processor.InputProcessor(), priority=1)
    oWorld.add_processor(processor.MovementProcessor(), priority=2)
    oWorld.add_processor(processor.RenderingProcessor(oScreen = oScreen), priority=3)

    # Player
    oWorld.create_entity(
        component.Velocity(x = 0, y = 0),
        component.Position(x = 40, y = 300),
        component.Size(iWidth = 32, iHeight = 32),
        component.Player()
    )

    #Screen
    oWorld.create_entity(
        component.Screen(oScreen = oScreen),
    )

    #Map
    # Creation de la matrice map, chaque 1 correspond a un mur, le 0 est un espace libre
    oWorld.create_entity(
        component.Map(
            aMap = [
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ],
            aRender = {
                0: (255, 255, 255),
                1: (0, 0, 0)
            }

        ),
    )

    # Creation des instances, un player et une victoire
    oMinion = Player(40, 300)
    oBanane = Victory(500, 30, False)
    aEntities.append(oMinion)
    aEntities.append(oBanane)


    # Tant que le jeu n'est pas quitte on cree un cycle
    while True:

        oWorld.process()

        oClock.tick(FPS)

# Declenche de la fonction principal
run()
