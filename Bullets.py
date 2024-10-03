import pygame
from settings import *
import math
import random
from random import choice


class Bullets(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, bullet_from):

        super().__init__()

        self.x, self.y, self.direction, self.bullet_from = x, y, direction, bullet_from
        self.speed = 12
        self.temp_image = pygame.image.load("item/bullet_fire.png").convert_alpha()
        self.image = pygame.transform.scale(self.temp_image, (20, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, player, enemy_group, bullet_group, world_data, tanks_group):

        self.rect.x += (self.direction * self.speed)
        # Check whether bullet going out of screen

        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()

        # bullet hit the walls
        for tile in world_data:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                self.kill()

        if self.bullet_from == "player":  # bullet from player
            # Bullet check damage
            for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, bullet_group, True):
                    if enemy.death is False:
                        self.kill()
                        player.score += 1
                        enemy.health -= 1

            # for destroying tank group
            for tank in tanks_group:
                if pygame.sprite.spritecollide(tank, bullet_group, True):
                    if tank.death is False:
                        self.kill()
                        player.score += 3
                        tank.health -= 1

        if pygame.sprite.spritecollide(player, bullet_group, True):
            if player.death is False:
                self.kill()
                player.health -= 1


class Grenade(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, ob_type):
        super().__init__()

        self.x, self.y, self.direction = x, y, direction
        self.ob_type = ob_type
        self.missile_dist = [-18, -16, -15, -14, -12, -11, -10, 8, 10]
        if self.ob_type == "bomb":
            self.vel_y = random.randint(-15, 0)
            self.temp_image = pygame.image.load("item/bomb.png").convert_alpha()

        elif self.ob_type == "missile":
            self.vel_y = random.randint(-25, -15)
            self.speed = choice(self.missile_dist)
            self.temp_image = pygame.image.load("item/grenade.png").convert_alpha()

        elif self.ob_type == "grenade":
            self.vel_y = -11
            self.speed = 5
            self.temp_image = pygame.image.load("item/grenade.png").convert_alpha()

        self.image = pygame.transform.scale(self.temp_image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.timer = 100  # time to start explosion
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.blow_sound = pygame.mixer.Sound("sound/explosion.wav")
        self.blow_sound.set_volume(1.5)

    def update(self, player, enemy_group, explosion_group, tanks_group, world_data, screen_scroll):
        dx = 0
        dy = 0

        # pygame.draw.rect(screen, RED, self.rect, 2)
        GRAVITY = 1
        # self.rect.x += (self.direction * self.speed)

        # if not bomb, if bomb dx=0
        if self.ob_type == "bomb":
            dx = 0
            self.vel_y += GRAVITY
            dy += self.vel_y
            if self.vel_y > 3:  # set terminal velocity
                self.vel_y = 3
        else:
            dx += self.direction * self.speed
            self.vel_y += GRAVITY

            if self.vel_y > 10:  # set terminal velocity
                self.vel_y = 10

            dy += self.vel_y

            # check for collision:
            for tile in world_data:
                # check for x direction collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    self.direction = -self.direction

                # check for y direction collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    # check if below ground (jumping)
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                        dx = 0

                    # check if on the ground (collide with tile and jump_vel =0 => on the ground)
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.jump = False  # reset key
                        dy = tile[1].top - self.rect.bottom  # touch on the ground
                        dx = 0

        self.rect.x += dx
        self.rect.x += screen_scroll
        self.rect.y += dy

        # set a timer for detonating bombs
        self.timer -= 1
        if self.timer <= 0:
            # when timer reached, to blow off
            pygame.mixer.Sound.play(self.blow_sound)
            self.kill()
            explode = Explosion(self.rect.x, self.rect.y)
            explosion_group.add(explode)

            # Grenade do damage to the players or enemy nearby

            if abs(self.rect.x - player.rect.centerx) < 80 and abs(self.rect.y - player.rect.centery) < 80:
                player.health -= 1

            for enemy in enemy_group:
                if abs(self.rect.x - enemy.rect.centerx) < 80 and abs(self.rect.y - enemy.rect.centery) < 80:
                    enemy.health -= 3
                    player.score += 1

            for tank in tanks_group:
                if abs(self.rect.x - tank.rect.centerx) < 80 and abs(self.rect.y - tank.rect.centery) < 80:
                    tank.health -= 3
                    player.score += 3


class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.x, self.y = x, y
        self.explosion_matrix = []
        for i in range(1, 6):
            self.temp_image = pygame.image.load(f"explosion/exp{i}.png").convert_alpha()
            self.image = pygame.transform.scale(self.temp_image, (60, 60))
            self.explosion_matrix.append(self.image)

        self.amt_index = 0
        self.image = self.explosion_matrix[self.amt_index]
        self.rect = self.image.get_rect()

        self.rect.center = (self.x, self.y)
        self.counter = 0

    def update(self, screen, screen_scroll):
        # pygame.draw.rect(screen, RED, self.rect, 2)
        self.rect.x += screen_scroll
        self.counter += 1
        if self.counter >= 5:
            self.counter = 0
            self.amt_index += 1
            self.image = self.explosion_matrix[self.amt_index]
            if self.amt_index >= len(self.explosion_matrix) - 1:
                self.kill()


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, ob_index):
        pygame.sprite.Sprite.__init__(self)

        self.x, self.y, self.ob_index = x, y, ob_index
        self.img = pygame.image.load(f"Tile/{self.ob_index}.png").convert_alpha()
        if self.ob_index == 8:
            self.image = pygame.transform.scale(self.img, (TILE_SIZE, TILE_SIZE // 2))
        else:
            self.image = pygame.transform.scale(self.img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, screen, screen_scroll):

        self.rect.x += screen_scroll


class Tanks(pygame.sprite.Sprite):

    def __init__(self, x, y, image_index):
        super().__init__()

        self.x, self.y, self.img_index = x, y, image_index
        self.img = pygame.image.load(f"Tile/{self.img_index}.png").convert_alpha()
        self.image = pygame.transform.scale(self.img, (TILE_SIZE * 1.5, TILE_SIZE))
        self.flip = False
        self.death = False

        # for bats attributes
        if self.img_index == 33:
            self.no_shoot = True  # they can shoot
            self.direction = 5
            self.enemy_cooltime = 1
            self.drop_bomb = False
            self.fly_direction = (-1.5, -1, 0, 1, 1.5)
            self.health = 1
            self.init_health = 1
            # for tanks attributes
        elif self.img_index == 13:
            self.no_shoot = False
            self.direction = 1
            self.enemy_cooltime = 20
            self.drop_bomb = False
            self.health = 10
            self.init_health = 10

            # for plane attributes
        elif self.img_index == 34:
            self.no_shoot = True  # they can shoot and drop bombs
            self.direction = -2
            self.enemy_cooltime = 1
            self.drop_bomb = True
            self.bomb_counter = 0
            self.health = 5
            self.init_health = 5
            # for turret attributes
        elif self.img_index == 32:
            self.no_shoot = True
            self.direction = 0  # no movement
            self.enemy_cooltime = 1
            self.drop_bomb = True
            self.bomb_counter = 0
            self.health = 3
            self.init_health = 3
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.counter = 0  # counter for direction change

        self.shoot_cooltime = 100  # time interval between shooting
        self.timer = 0  # delay the bullet moving

    def update(self, screen_scroll):

        # dice = random.randint(0, 100)

        if self.timer > self.enemy_cooltime:  # sets timer and control tank move speed
            self.timer = 0
            if self.img_index == 33:  # bats movement, up/down
                self.rect.x += self.direction
                self.rect.y -= self.direction * choice(self.fly_direction)  # vertical route monster
                if self.rect.y < 0: self.rect.y = 10  # limit the distance of bats that can move

            else:
                self.rect.x += self.direction  # horizontal movement enemy

            self.counter += 1

            if self.img_index != 34:  # change direction only for not 34, for not plane
                if abs(self.counter) > 20:
                    self.direction = -self.direction  # change direction when the counter reach 50
                    self.counter *= -1  # change the counter to negative and then add back to positive
            elif self.rect.x < 0:
                self.rect.x = 1600

        self.timer += 1

        self.rect.x += screen_scroll

    def shoot(self, missile_group):

        if self.shoot_cooltime <= 0:
            self.shoot_cooltime = 300
            magnitude = 15
            angle = random.randint(0, 360)
            missile = Missile(self.rect.centerx, self.rect.centery, magnitude, angle)
            missile_group.add(missile)

        self.shoot_cooltime -= 1

    def health_bar(self, x, y, max_health, screen, bar_width, bar_height):

        pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, YELLOW, (x, y, bar_width * (self.health / max_health), bar_height))


class Missile(pygame.sprite.Sprite):

    def __init__(self, x, y, magnitude, angle):

        super().__init__()

        self.x, self.y = x, y
        self.mag, self.angle = magnitude, angle
        self.img = pygame.image.load("item/firepower.png")
        self.image = pygame.transform.scale(self.img, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = ["top", "bottom"]
        self.counter = 0
        self.ready_to_fire = True
        self.dx, self.dy = 0, 0

    def update(self, player, tank, screen_scroll, missile_group):

        if self.counter > 10:
            self.counter = 0

            # determine direction of firepower from the tank
            if self.ready_to_fire:
                self.ready_to_fire = False
                missile_direction = choice(self.direction)
                # case 1 : player is at the lower left hand corner
                if missile_direction == "bottom":  # image tank shift downward
                    self.dx = -abs(float(self.mag * math.cos(self.angle)))
                    self.dy = abs(float(self.mag * math.sin(self.angle)))

                elif missile_direction == "top":
                    self.dx = -abs(float(self.mag * math.cos(self.angle)))
                    self.dy = -abs(float(self.mag * math.sin(self.angle)))

            self.rect.x += self.dx
            self.rect.y += self.dy

        self.counter += 1

        if self.rect.x < 0 or self.rect.y < 0 or abs(self.rect.x - player.rect.x) > 800 or \
                abs(self.rect.y - player.rect.y) > 640:
            # if out of screen, the sprite is killed
            self.ready_to_fire = True
            self.kill()

        # checking collision between player and the missile

        if pygame.sprite.spritecollide(player, missile_group, False):
            self.kill()  # missile disappear on hit
            player.health -= 2
