import pygame,json 

NEIGHBOURS=[(-1,0),(0,-1),(1,0),(0,1)]
PHYSICS_TILES=[]

class Tilemap:
    def __init__(self,game,tile_size=30):
        self.game=game 
        self.tile_size=tile_size 
        self.tile_map={}
        self.offgridtiles=[] 

    def extract(self,id_pairs,keep=False):
        matches=[]
        for tile in self.offgridtiles.copy():
            if (tile['type'],tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgridtiles.remove(tile) 
        locs_to_delete=[]
        for loc in self.tile_map:
            tile=self.tile_map[loc]
            if(tile['type'],tile['variant']) in id_pairs:
                tile_copy={'type':tile['type'],'variant':tile['variant'],'pos':(tile['pos'][0],tile['pos'][1])}
                if not keep:
                    locs_to_delete.append(tile)
                matches.append(tile_copy)
        for loc_to_delete in locs_to_delete:
            del self.tile_map[loc_to_delete]
        return matches
    
    def tiles_around(self,pos):
        tiles=[]
        tile_loc=(int(pos[0]//self.tile_size),int(pos[1]//self.tile_size))
        for a,b in NEIGHBOURS:
            check_loc=str(tile_loc[0]+a)+';'+str(tile_loc[1]+b)
        if check_loc in self.tile_map:
            tiles.append(self.tile_map[check_loc])
        return tiles
    
    def save(self,path):
        f=open(path,'w')
        json.dump({'tilemap':self.tilemap,'tile_size':self.tile_size,'offgrid_tiles':self.offgrid_tiles},f)
        f.close()

    def load(self,path):
        f=open(path,'r')
        map_data=json.load(f)
        f.close()
        self.tilemap=map_data['tilemap']
        self.tile_size=map_data['tile_size']
        try:
            self.offgrid_tiles=map_data['offgrid_tiles']
        except:
            self.offgrid_tiles=map_data['offgrid']

    def solid_check(self,pos):
        tile_loc= str(int(pos[0]//self.tile_size))+';'+str(int(pos[1]//self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]
        return False 
    
    def physics_rects_around(self,pos):
        rects=[]
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0]*self.tile_size,
                                         tile['pos'][1]*self.tile_size,
                                         self.tile_size,
                                         self.tile_size
                                         )
                            )
        return rects
    
    def render(self,surf,offset=(0,0)):
        pass