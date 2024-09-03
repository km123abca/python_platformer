import sys
import pygame 
from scripts.utils import monitor_input,load_images
from scripts.Tilemap import Tilemap
RENDER_SCALE=1.0

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Platformer')
        self.screen=pygame.display.set_mode((640,480))
        self.display=pygame.Surface((640,480))
        self.clock=pygame.time.Clock()
        self.clicking=[False,False] #left is mouse left click
        self.key_set=set()
        self.assets={
                     'platforms':load_images('platforms')
                    }
        self.tile_map=Tilemap(self,tile_size=16)
        try:
            self.tilemap.load('map.json')
        except:
            pass

    def run(self):
        print('game has started')
        while True:
            self.display.fill((0,0,0,0))
            monitor_input(self)
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()
            self.clock.tick(60)

game=Game()
game.run()
