import pygame
import sys 
from Scripts.entities import PhysicsEntity, Player
from Scripts.utils import load_image, load_images, Animation
from Scripts.tilemap import Tilemap
from Scripts.clouds import Clouds


class Game: 
    def __init__(self):     
        pygame.init()

        pygame.display.set_caption('ninja game')
        self.screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

        # movement var
        self.movement = [False, False]
        # assets here 
        self.assets = {
            'player': load_image('entities/player.png'),
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone') ,
            'background': load_image('background.png'),
            'clouds' : load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')), 
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),


        }

        self.clouds = Clouds(self.assets['clouds'], count = 24)

        self.player = Player(self , (50,50), (8,15))
        
        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0,0]

    def run(self):
        while True: 
            # make screen background here 
            self.display.blit(self.assets['background'], (0,0))
            #set camera to track player ## this is x axis
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0]) / 30
            #set camera to track player on Y axis
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1])/ 30
            
            render_scroll = (int(self.scroll[0]) ,int(self.scroll[1]))  
            # render clouds before tilemap
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            # render tilemap behind player and add camera offset
            self.tilemap.render(self.display, offset=render_scroll)
            #render player here
            self.player.update(self.tilemap, (self.movement[1]-self.movement[0],  0))
            self.player.render(self.display,  offset=self.scroll)

            print(self.tilemap.physics_rects_around(self.player.pos))
            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit() 
                ## Button event handlers for menu 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True 
                    if event.key == pygame.K_d:
                        self.movement[1] = True  
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_a: 
                        self.movement[0] = False
                    if event.key == pygame.K_d: 
                        self.movement[1] = False

        

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60) 
Game().run()