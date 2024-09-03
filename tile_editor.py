import sys
import pygame 
from scripts.utils import load_images
from scripts.Tilemap import Tilemap
RENDER_SCALE=1.0

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tile Editor')
        self.screen=pygame.display.set_mode((640,480))
        self.display=pygame.Surface((640,480))
        self.clock=pygame.time.Clock()
        self.clicking=[False,False] #0 is mouse left click
        # self.key_set=set() used in game
        self.assets={
                     'platforms':load_images('platforms')
                    }
        self.scroll=[0,0]
        self.tile_list=list(self.assets)
        self.tile_group=0
        self.tile_variant=0
        self.shift=False
        self.ongrid=True
        self.movement=[0,0,0,0]
        self.tile_size=64
        self.tile_map=Tilemap(self,tile_size=self.tile_size)
        try:
            self.tile_map.load('map.json')
            print('loaded from map')
        except:
            print('did not find map.json')
            pass
        self.movement=[0,0,0,0]
    def run(self):
        print('Editor has started')
        while True:
            self.display.fill((0,0,0,0))
            #updating camerascroll based on movement (which is in turn controlled by arrow keys)
            self.scroll[0]+=(self.movement[2]-self.movement[0])*RENDER_SCALE
            self.scroll[1]+=(self.movement[3]-self.movement[1])*RENDER_SCALE
            render_scroll=[int(self.scroll[0]),int(self.scroll[1])]
            self.tile_map.render(self.display,offset=render_scroll)
            #updating camerascroll based on movement (which is in turn controlled by arrow keys) ends
            #displayiing a transparent version of the selected tile
            current_tile_img=self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
            self.display.blit(pygame.transform.scale(current_tile_img,(self.tile_size,self.tile_size)),
                              (16,16))
            #displayiing a transparent version of the selected tile 
            mpos=pygame.mouse.get_pos()
            mpos=(mpos[0]/RENDER_SCALE,mpos[1]/RENDER_SCALE)
            tile_pos=(int((self.scroll[0]+mpos[0])/self.tile_map.tile_size),int((self.scroll[1]+mpos[1])/self.tile_map.tile_size))
            if self.ongrid:
                self.display.blit(pygame.transform.scale(current_tile_img,(self.tile_size,self.tile_size)),
                                  (tile_pos[0]*self.tile_map.tile_size-self.scroll[0],tile_pos[1]*self.tile_map.tile_size-self.scroll[1]))
            else:
                self.display.blit(pygame.transform.scale(current_tile_img,(self.tile_size,self.tile_size)),
                                  mpos)
            if self.clicking[0] and self.ongrid:
                self.tile_map.tile_map[str(tile_pos[0])+';'+str(tile_pos[1])]={'type':self.tile_list[self.tile_group],'variant':self.tile_variant,'pos':tile_pos}
            if self.clicking[1]:
                tile_loc=str(tile_pos[0])+';'+str(tile_pos[1])
                if tile_loc in self.tile_map.tile_map:
                    del self.tile_map.tile_map[tile_loc]
                for tile in self.tile_map.offgrid_tiles.copy():
                    tile_rect=pygame.Rect(tile['pos'][0]-self.scroll[0],tile['pos'][1]-self.scroll[1],
                                          self.tile_map.tile_size,self.tile_map.tile_size
                                          )
                    if tile_rect.collidepoint(mpos):
                        self.tile_map.offgrid_tiles.remove(tile)
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #monitoring keydown and up
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LSHIFT:
                        self.shift=True
                    if event.key==pygame.K_DOWN:
                        self.movement[3]=1
                    if event.key==pygame.K_UP:
                        self.movement[1]=1
                    if event.key==pygame.K_RIGHT:
                        self.movement[2]=1 
                    if event.key==pygame.K_LEFT:
                        self.movement[0]=1
                    if event.key==pygame.K_g:
                        self.ongrid=not self.ongrid 
                    if event.key==pygame.K_o:
                        self.tile_map.save('map.json')
                    
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_LSHIFT:
                        self.shift=False 
                    if event.key==pygame.K_DOWN:
                        self.movement[3]=0
                    if event.key==pygame.K_UP:
                        self.movement[1]=0
                    if event.key==pygame.K_RIGHT:
                        self.movement[2]=0 
                    if event.key==pygame.K_LEFT:
                        self.movement[0]=0
                #monitoring keydown and up ends
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        self.clicking[0]=True                        
                        if not self.ongrid:
                            self.tile_map.offgrid_tiles.append({'type':self.tile_list[self.tile_group],'variant':self.tile_variant,'pos':(mpos[0]+self.scroll[0],mpos[1]+self.scroll[1])})
                    if event.button==3:
                        self.clicking[1]=True 
                    if event.button==4:
                        print('scrolled')
                        if self.shift:
                            self.tile_variant=(self.tile_variant-1)%len(self.assets[self.tile_list[self.tile_group]])
                        else:
                            self.tile_group=(self.tile_group-1)%len(self.tile_list)
                            self.tile_variant=0
                    if event.button==5:
                        if self.shift:
                            self.tile_variant=(self.tile_variant+1)%len(self.assets[self.tile_list[self.tile_group]])
                        else:
                            self.tile_group=(self.tile_group+1)%len(self.tile_list)
                            self.tile_variant=0
                if event.type==pygame.MOUSEBUTTONUP:
                    if event.button==1:
                        self.clicking[0]=False 
                    if event.button==3:
                        self.clicking[1]=False
                        
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()
            self.clock.tick(60)

game=Game()
game.run()
