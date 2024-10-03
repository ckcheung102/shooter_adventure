import pygame
import pickle
from settings import *
from Player import Gunner
from Bullets import Grenade, Obstacle, Tanks
from Item import Itembox


game_lives=3

# sprite Group definition
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
tanks_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()



class Tile:

    def __init__(self):

        self.world_data = []
        self.tile_image = []
        self.display_img = []

        self.display_surface = pygame.display.get_surface()

    def load_tiles(self, level, last_score):

        global player, box
        for i in range(0, num_image):
            item_img = pygame.image.load(f"Tile/{i}.png").convert_alpha()
            self.tile_image.append(item_img)

        pickle_in = open(f'level/level{level}_data.csv', 'rb')
        graph_data = pickle.load(pickle_in)

        print(graph_data)
        for y, row in enumerate(graph_data):
            for x, col in enumerate(row):
                # spare 35
                if 0 <= col < 12 or (20 < col < 31):
                    self.store_tiles(self.tile_image[col], x, y, col)
                    # rect_img = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 32, 32)

                # stationary enemy
                elif col == 18 or col == 19 or (35 < col < 38):
                    obstacle = Obstacle(x * TILE_SIZE, y * TILE_SIZE, col)
                    obstacle_group.add(obstacle)

                # moving enemy with missiles
                elif col == 13 or col == 33 or col == 32 or col == 34:
                    tank = Tanks(x * TILE_SIZE, y * TILE_SIZE, col)
                    tanks_group.add(tank)

                # Enemy gunner with AI
                elif col == 15 and game_lives > 0:  # when no more lives, no need to create instance of enemy
                    enemy = Gunner(x * TILE_SIZE, y * TILE_SIZE, "enemy1", scale, 2, 20, 0, 3, 0)
                    enemy_group.add(enemy)

                # player
                elif col == 14 and game_lives > 0:  # when no more lives, no need to create instance of player
                    player = Gunner(x * TILE_SIZE, y * TILE_SIZE, "player", scale, player_speed,
                                    AMMON, GRENADE, max_health, last_score)


                # Item box
                elif (15 < col < 18) or col == 38 or col == 20 or col == 39:
                    if col == 16:
                        box = Itembox(x * TILE_SIZE, y * TILE_SIZE, "bullet")

                    elif col == 17:
                        box = Itembox(x * TILE_SIZE, y * TILE_SIZE, "grenade")
                    elif col == 38:
                        box = Itembox(x * TILE_SIZE, y * TILE_SIZE, "chopper")
                    elif col == 20:
                        box = Itembox(x * TILE_SIZE, y * TILE_SIZE, "heart")
                    elif col == 39:
                        box = Itembox(x * TILE_SIZE, y * TILE_SIZE, "life")

                    item_group.add(box)

        return player

    def store_tiles(self, image, x, y, img_index):

        tile_image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        tile_rect = tile_image.get_rect()
        tile_rect.x = x * TILE_SIZE
        tile_rect.y = y * TILE_SIZE
        tiles = (tile_image, tile_rect)
        # display images only
        if (10 < img_index < 12) or (20 < img_index < 23):  # 11,12,21,22 are images only
            self.display_img.append(tiles)  # no interacting with player
        else:
            self.world_data.append(tiles)

    def draw_tiles(self, screen):

        for tile in self.world_data:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

        for tile in self.display_img:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
