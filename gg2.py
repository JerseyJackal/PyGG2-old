import pygame
from pygame.locals import *
from gameobject import MapObject, PlayerControl
from Character import Scout
from collision import objectCheckCollision, characterHitObstacle
from functions import sign, place_free, point_direction

class GG2:
    """
    Central class
    """
    
    # This is to replace the gmk "all" and also to update everything.
    GameObjectList = []
    
    Xview = 0
    Yview = 0
    
    def __init__(self):
        pygame.init()
        
        # All drawing should be done on the Surface object
        self.Window = pygame.display.set_mode((800, 600))
        self.Surface = pygame.display.get_surface()
        
        self.Wview = self.Window.get_width()
        self.Hview = self.Window.get_height()
        
        self.gameMap = MapObject(self)
        self.PlayerControl = PlayerControl(self)
        self.Myself = Scout(self)

        self.clock = pygame.time.Clock()
        
    def step(self):
        #'Steps' the engine. Twisted will step this at some point.

        self.clock.tick(30)
        
        for obj in self.GameObjectList:    obj.beginStep()
        for obj in self.GameObjectList:    obj.step()
        for obj in self.GameObjectList:    obj.endStep()

        self.Xview = self.Myself.x - self.Wview/2
        self.Yview = self.Myself.y - self.Hview/2

        for obj in self.GameObjectList:    obj.collide()

        for obj in self.GameObjectList:
            if obj.destroyInstance:
                obj.destroy()

        self.Surface.fill((255, 255, 255))

        for obj in self.GameObjectList: obj.draw()

        pygame.display.flip()
