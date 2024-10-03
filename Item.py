import pygame as pg
from settings import *


class Itembox(pg.sprite.Sprite):

    def __init__(self, x, y, item_type):

        pg.sprite.Sprite.__init__(self)

        item_image = []
        self.x = x
        self.y = y
        self.item_type = item_type
        self.bullet = 0
        self.grenade = 0

        img_dict = {
            'bullet': 0,
            'grenade': 1,
            'heart': 2,
            'chopper': 3,
            'life': 4
        }

        for i in range(0, 5):
            temp_img = pg.image.load(f"item/{item_type}.png").convert_alpha()
            if self.item_type == "chopper":
                image_box = pg.transform.scale(temp_img, (3 * TILE_SIZE, 3 * TILE_SIZE))
            else:
                image_box = pg.transform.scale(temp_img, (TILE_SIZE, TILE_SIZE))
            item_image.append(image_box)  # 0 - bullet, 1- grenade

        self.image = item_image[img_dict[self.item_type]]
        self.rect = self.image.get_rect()
        if self.item_type == "chopper":
            self.rect.midleft = (self.x, self.y)
        else:
            self.rect.x = self.x
            self.rect.y = self.y

    def update(self, player, screen_scroll, item_group):

        self.rect.x += screen_scroll

        if self.item_type != "chopper":
            if pg.sprite.collide_rect(self, player):

                if self.item_type == "bullet":
                    player.ammon += 1

                elif self.item_type == "grenade":
                    player.grenade += 1

                elif self.item_type == "heart":
                    player.health += 2

                elif self.item_type == "life":
                    player.add_live = True

                self.kill()

        else:

            if pg.sprite.collide_rect(self,player) :

                print("yes")
                player.win = True




class moving_blocks(pg.sprite.Sprite):

    def init(self, x, y, move_type):
        super().__init__()

        self.x, self.y = x, y
        self.move_type = move_type

        self.direction = 1
        self.cd_counter = 100
