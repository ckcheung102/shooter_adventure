from Bullets import Bullets
from settings import *
import random


class Gunner(pygame.sprite.Sprite):

    def __init__(self, x, y, character, scale, speed, ammon, grenade, health, last_score, timer):

        super().__init__()

        self.character = character
        self.health = health
        self.jump = False
        self.in_air = False
        self.jump_vel = 0

        self.death = False
        self.action_type = {"idle": 5, "run": 6, "jump": 1, "death": 6}  # no. of frames per dict
        self.animation_list = []
        self.amt_index = 0
        self.action = 0

        # player modes - death, idle, jump , run
        modes = ["Idle", "Run", "Jump", "Death"]
        # 0 - Idle, 1-Run, 2-Jump, 3 - Death

        self.mode_frame = {"Idle": 5, "Run": 10, "Jump": 9, "Death": 10}

        self.animation_processing(modes, scale)

        # version 2 image processing  for player

        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.scale_img = self.animation_list[self.action][self.amt_index]
        self.rect = self.scale_img.get_rect()
        self.rect.center = (x, y)
        self.width = self.scale_img.get_width()
        self.height = self.scale_img.get_height()

        self.update_time = pygame.time.get_ticks()

        self.timer = timer

        self.shoot_cooldown = 0
        self.ammon = ammon
        self.start_ammon = ammon
        self.grenade = grenade

        self.body_erase = False

        # enemy AI counter
        self.move_counter = 0
        self.idling = False
        self.idle_counter = 0

        self.vision_rect = pygame.Rect(0, 0, 300, self.scale_img.get_height())
        self.win = False
        self.dead_counter = 0

        self.add_live = False
        self.score = last_score  # player score

        self.jump_sound = pygame.mixer.Sound("sound/jump.mp3")
        self.shoot_sound = pygame.mixer.Sound("sound/shoot1.wav")

        self.climb_speed = 1
        self.jump_count = 0

        self.collided_rects = []

        self.on_hit = {"left_wall": False,
                       "right_wall": False}

    def check_hit_wall(self, world_data):
        left_rect = pygame.Rect(self.rect.left - 2, self.rect.top + 1 / 4 * self.rect.height, 2, 1 / 2 * self.height)
        right_rect = pygame.Rect(self.rect.right, self.rect.top + 1 / 4 * self.rect.height, 2, 1 / 2 * self.height)

        # Debugging purpose
        # pygame.draw.rect(screen, "blue", left_rect)
        # pygame.draw.rect(screen, "blue", right_rect)

        self.collided_sprites = [tile[1] for tile in world_data]
        self.on_hit["left_wall"] = True if left_rect.collidelist(self.collided_sprites) >= 0 else False
        self.on_hit["right_wall"] = True if right_rect.collidelist(self.collided_sprites) >= 0 else False

    def move(self, move_left, move_right, world_data):

        screen_scroll = 0
        dx = 0
        dy = 0

        GRAVITY = 1

        if self.character == "player" or self.character == "enemy1":

            if move_left:
                self.flip = True
                self.direction = -1
                dx += self.speed * self.direction

            elif move_right:
                self.flip = False
                self.direction = 1
                dx += self.speed * self.direction

            self.check_hit_wall(world_data)
            # when player input jump first time,

            if self.jump:
                self.jump = False
                if not self.in_air:  # if on the floor
                    self.in_air=True
                    self.jump_vel = -16

                elif any((self.on_hit["left_wall"], self.on_hit["right_wall"])):    # in air
                    # side jump
                    self.timer.timer_on()
                    self.jump_count += 1  # record no. of side jump
                    if self.jump_count > 1:
                        pygame.draw.rect(screen, "red", self.rect)
                    #self.direction = 1 if self.on_hit["left_wall"] else -1  # bounce off opposite dir

            # Handling Action
            #  Jumping at walls
            if self.in_air and any((self.on_hit["left_wall"], self.on_hit["right_wall"])) \
                   and self.timer.active and self.jump_count < 3:
                self.jump_vel =-16
                print("touching walls")

            # Falling function
            else:

                self.jump_vel += GRAVITY

                if self.jump_vel > 10:
                    self.jump_vel = 10  # until reaching terminal velocity
                # then add gravity to go down
                dy += self.jump_vel
                print("falling")

            # check for collision:
            for tile in world_data:

                # check for x direction collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # check for y direction collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    # check if below ground (jumping)
                    if self.jump_vel < 0:
                        self.jump_vel = 0
                        dy = tile[1].bottom - self.rect.top

                    # check if on the ground (collide with tile and jump_vel =0 => on the ground)
                    elif self.jump_vel >= 0:
                        self.jump_vel = 0
                        self.in_air = False
                        self.jump_count = 0

                        dy = tile[1].top - self.rect.bottom  # touch on the ground

            # moving blocks
            if not self.death:
                self.rect.x += dx
                self.rect.y += dy

            # scrolling update based on player position
            if self.character == "player":
                if self.rect.right > SCREEN_WIDTH - scroll_range and self.death is False:
                    self.rect.x -= dx
                    screen_scroll = -dx

                if self.rect.left < screen_scroll + 10:  # limit the scrolling back
                    self.rect.x -= dx
                    screen_scroll = 0

        return screen_scroll

    def shoot(self, bullet_group):

        if self.shoot_cooldown == 0 and self.ammon > 0:
            self.shoot_cooldown = 25
            bullet = Bullets(self.rect.centerx + 0.9 * (self.rect.size[0] * self.direction), self.rect.centery,
                             self.direction, self.character)
            bullet_group.add(bullet)
            self.ammon -= 1  # each shooting reduce by 1
        self.shoot_cooldown -= 1
        if self.shoot_cooldown < 0:
            self.shoot_cooldown = 0

    def update_animation(self):
        # update animation

        animation_cooldown = 100

        # check latest time passed cooldown or not
        current_time = pygame.time.get_ticks()

        self.scale_img = self.animation_list[self.action][self.amt_index]

        if current_time - self.update_time >= animation_cooldown:
            self.amt_index += 1
            self.update_time = current_time  # new time
            if self.amt_index >= len(self.animation_list[self.action]):  # reach the end of index
                if self.death is True:
                    self.amt_index = len(self.animation_list[self.action]) - 1
                    self.body_erase = True
                else:
                    self.amt_index = 0

    def revise_action(self, new_action):
        # check if action needs to change or not
        if self.action != new_action:
            self.action = new_action
            self.amt_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_death(self, obstacle_group, tanks_group):

        # instant dead condition
        if pygame.sprite.spritecollide(self, obstacle_group, False) or \
                pygame.sprite.spritecollide(self, tanks_group, False) or \
                self.rect.y > 800:
            self.health = 0

        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.death = True

            self.revise_action(3)
            if self.body_erase:  # make sure dead animation finished before removing the sprite on screen
                self.kill()

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        screen.blit(pygame.transform.flip(self.scale_img, self.flip, False), self.rect)
        # pygame.draw.line(screen, RED, (0, 200 + self.rect.height // 2), (800, 200 + self.rect.height // 2))

    def health_bar(self, x, y, max_health, screen, bar_width, bar_height):

        pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, YELLOW, (x, y, bar_width * (self.health / max_health), bar_height))

    def ai(self, player, bullet_group, world_data, screen_scroll):

        chose_to_move = random.randint(0, 100)
        if not self.death and player.death is False:

            # Check enemy is in idle :

            if self.idling is False and chose_to_move < 3:  # 1,2 was chosen, then becomes idle
                self.idling = True
                self.idle_counter = 50
                self.revise_action(0)

            self.idle_counter -= 1  # idle counter reduce by 1
            if self.idle_counter <= 0:
                self.idle_counter = 0
                self.idling = False
                self.revise_action(1)

            # Patrolling
            if self.idling is False:
                # Patrolling when idle is false
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right, world_data)
                self.revise_action(1)
                self.update_animation()
                self.move_counter += 1

                if self.character == "enemy1":
                    # setup vision for enemy
                    self.vision_rect.center = (self.rect.centerx + 100 * self.direction, self.rect.centery)
                    # pygame.draw.rect(screen, RED, self.vision_rect, 2)
                    # check if enemy vision collide with player
                    if self.vision_rect.colliderect(player.rect):
                        # if yes, shoot

                        self.shoot(bullet_group)

                    elif self.move_counter > TILE_SIZE // 3 or self.rect.colliderect(player):
                        # check boundary/ and change direction after time passed

                        self.move_counter *= -1
                        self.direction = -self.direction

            # enemy move based on screen scroll
            self.rect.x += screen_scroll

        elif player.death is True:  # if player is dead, enemy is idle

            self.idle = True
            self.revise_action(0)

    def animation_processing(self, modes, scale):

        # assign images into animation list
        if self.character == "enemy1":
            for action in self.action_type:  # 4 modes: 0- idle -> 1- run -> 2- jump -> 3- death
                temp_list = []  # declares the temp list is a list
                for j in range(self.action_type[action]):
                    self.image = pygame.image.load(f"{self.character}/{action}/{j}.png").convert_alpha()
                    self.scale = scale
                    self.scale_img = pygame.transform.scale(self.image, (self.scale * self.image.get_width(),
                                                                         self.scale * self.image.get_height()))
                    temp_list.append(self.scale_img)
                self.animation_list.append(temp_list)

        elif self.character == "player":
            # version 2 image processing  for player
            for i, mode in enumerate(modes):
                sprite_sheet = pygame.image.load(f"player/john/{mode}.png").convert_alpha()
                temp_list = []
                for j in range(self.mode_frame[mode]):
                    temp_img = sprite_sheet.subsurface(j * 26, 0, 26, 22)
                    scale_img = pygame.transform.scale(temp_img, (40, 40))
                    temp_list.append(scale_img)

                self.animation_list.append(temp_list)
