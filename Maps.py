import pygame
from settings import *
import pickle
from Player import Gunner


class Tile():

    def __init__(self):

        self.world_data=[]
        self.tile_image= []
        self.display_img=[]

        self.display_surface = pygame.display.get_surface()

    def load_tiles(self,level,enemy_group):

        global player, grenade_box, health_box
        for i in range(0, 37):
            item_img= pygame.image.load(f"Tile/{i}.png").convert_alpha()
            self.tile_image.append(item_img)


        pickle_in = open(f'level/level{level}_data.csv', 'rb')
        graph_data= pickle.load(pickle_in)
        print(graph_data)
        for y, row in enumerate(graph_data):
            for x, col in enumerate(row):

                if  0 < col < 7 or col == 10 or col > 21:
                    self.store_tiles(self.tile_image[col], x, y, col)
                    # rect_img = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 32, 32)

                if col==14:
                    player = Gunner(x*TILE_SIZE,y*TILE_SIZE, "player", scale, 5, AMMON, GRENADE)



                if col==15:
                        enemy=Gunner(x*TILE_SIZE,y*TILE_SIZE,"enemy1", scale, 2,20,0)
                        enemy_group.add(enemy)



    def store_tiles(self, image, x, y, img_index ):

        tile_image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        tile_rect = tile_image.get_rect()
        tile_rect.x = x * TILE_SIZE
        tile_rect.y = y * TILE_SIZE
        tiles = (tile_image, tile_rect)
        self.world_data.append(tiles)
        #self.display_img.append(tile_image)

    def draw_tiles(self, screen):

       for tile_image, tile_rect in self.world_data:
            screen.blit(tile_image, tile_rect)




