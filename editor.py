import pygame
import sys 
from Scripts.entities import PhysicsEntity 
from Scripts.utils import load_image, load_images 
from Scripts.tilemap import Tilemap 
RENDER_SCALE = 2.0 ##const for rendering 

class Editor: 
    def __init__(self):     
        pygame.init()

        pygame.display.set_caption('Level Editor')
        self.screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

       
        # assets here 
        self.assets = { 
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone') , 
        }
        # movement var
        self.movement = [False, False, False, False]
          
        self.tilemap = Tilemap(self, tile_size=16) 
        
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.scroll = [0,0]

        self.tile_list = list(self.assets) #hold available assets here
        self.tile_group = 0
        self.tile_variant = 0
        self.clicking = False
        self.rightClick = False
        self.shift = False
        self.ongrid = True

    def run(self):
        while True: 
            # make screen background here 
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2 
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, offset= render_scroll)

            curTileImg = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            curTileImg.set_alpha(100)

            mauspoz = pygame.mouse.get_pos()
            mauspoz = (mauspoz[0] / RENDER_SCALE, mauspoz[1] / RENDER_SCALE) 
            tilepoz = (int((mauspoz[0] + self.scroll[0]) // self.tilemap.tile_size), int((mauspoz[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(curTileImg, (tilepoz[0] * self.tilemap.tile_size - self.scroll[0], tilepoz[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(curTileImg, mauspoz)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tilepoz[0]) + ';' + str(tilepoz[1])] = {'type' : self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos': tilepoz}
           
            if self.rightClick:
                tile_loc = str(tilepoz[0]) + ';' + str(tilepoz[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']] #get tile imgs
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height()) #hitbox calc
                    if tile_r.collidepoint(mauspoz):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(curTileImg, (5, 5))  #displays currently selected tile in top left corner

            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit() 
                ##Mouse buttons here
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type' : self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos': (mauspoz[0] + self.scroll[0], mauspoz[1] + self.scroll[1])})
                    if event.button == 3:
                        self.rightClick = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])               
                    else: 
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.rightClick = False

                #keyboard keys here
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: #left
                        self.movement[0] = True 
                    if event.key == pygame.K_d: #right
                        self.movement[1] = True  
                    if event.key == pygame.K_w: # up 
                        self.movement[2] = True
                    if event.key == pygame.K_s:#downs
                        self.movement[3] = True
                    if event.key == pygame.K_g: #press g to snap to grid
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_t: 
                        self.tilemap.autotile()
                    if event.key == pygame.K_LSHIFT: #shift
                        self.shift = True

                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_a: #left
                        self.movement[0] = False
                    if event.key == pygame.K_d: #right
                        self.movement[1] = False
                    if event.key == pygame.K_w: # up 
                        self.movement[2] = False
                    if event.key == pygame.K_s:#down
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False  

        

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60) 
Editor().run()