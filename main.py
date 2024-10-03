from Player import Gunner
from Bullets import Grenade, Obstacle, Tanks
from settings import *
import pickle
from Button import Button
from Item import Itembox
from Movie import *
from Timer import Timer

pygame.init()
end_level = 8
bg_img = []

game_icon = pygame.image.load("Tile/39.png")
pygame.display.set_icon(game_icon)
pygame.display.set_caption("CK Game - Survival in Wild")
screen = screen


# loading background
for i in range(0, bg_num):
    background1 = pygame.image.load(f"background/new_scene/bg-{i}.png").convert_alpha()
    bg = pygame.transform.scale(background1, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img.append(bg)

font = pygame.font.SysFont('Roman', 25, bold=True)
font_win = pygame.font.Font("font/Filepile.otf", 10)
font1 = pygame.font.SysFont('Arial', 15, bold=True)

# dialog
dialog1 = pygame.image.load("item/dialog2.png").convert_alpha()
dialog1 = pygame.transform.scale(dialog1, (300, 100))

# Creating instances of players and item boxes :
# player = Gunner(0, 0, "player", scale, 5, AMMON, GRENADE)
# initialize parameters
level = 0
screen_scroll = 0
total_scroll = 0
game_lives = 3
# boolean setting
move_left = False
move_right = False
shoot = False
timer = Timer(300)

grenade_throw = False
running = True
clear_to_count = False

clock = pygame.time.Clock()
FPS = 70
count_time = 0

last_score = 0

# sprite Group definition
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
tanks_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

waypoints = [
    (100, 100),
    (700, 200),
    (430, 100),
    (300, 300),
    (100, 100)

]
#boss_group = pygame.sprite.Group()
#temp_boss_img = pygame.image.load("Tile/38.png")
#boss_img = pygame.transform.scale(temp_boss_img, (40, 40))
#boss = Boss(boss_img, waypoints, 0)
#boss_group.add(boss)





# create the boss group, and create instance of boss

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


        for y, row in enumerate(graph_data):
            for x, col in enumerate(row):
                # spare 35
                if 0 <= col < 13 or (20 < col < 31):
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
                    enemy = Gunner(x * TILE_SIZE, y * TILE_SIZE, "enemy1", scale, 2, 20, 0, 3, 0, timer)
                    enemy_group.add(enemy)

                # player
                elif col == 14 and game_lives > 0:  # when no more lives, no need to create instance of player
                    player = Gunner(x * TILE_SIZE, y * TILE_SIZE, "player", scale, player_speed,
                                    AMMON, GRENADE, max_health, last_score, timer)

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
        if (10 < img_index < 13) or (20 < img_index < 23):  # 11,12,21,22 are images only
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


def update_timer():
    timer.update()


def get_input():
    # keyboard input
    global move_left, move_right, shoot, grenade_throw, running

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type==pygame.KEYDOWN:

            if event.key==pygame.K_LEFT:
                move_left = True
            if event.key==pygame.K_RIGHT:
                move_right = True

            if event.key==pygame.K_SPACE and player.death is False:
                player.jump = True

                pygame.mixer.Sound.play(player.jump_sound)
            if event.key==pygame.K_s:
                shoot = True

            if event.key==pygame.K_f:
                grenade_throw = True

            if event.key==pygame.K_ESCAPE:
                running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_SPACE:
                player.jump = False

            if event.key == pygame.K_s:
                shoot = False


def check_player_action():
    global grenade_throw, screen_scroll, total_scroll

    if player.death is False:

        # blit the no. of lives on screen
        for j in range(0, game_lives):
            screen.blit(player.animation_list[0][0], (800 - 30 * j, 10))

        # Player motion
        screen_scroll = player.move(move_left, move_right, tile.world_data)
        total_scroll += screen_scroll

        if shoot and player.ammon > 0:
            player.shoot(bullet_group)
            pygame.mixer.Sound.play(player.shoot_sound)
        elif grenade_throw and player.grenade > 0:  # when player has enough grenades
            grenade = Grenade(player.rect.centerx + (0.3 * player.rect.size[0] * player.direction),
                              player.rect.centery - 0.5 * player.rect.size[1], player.direction, "grenade")
            grenade_group.add(grenade)
            player.grenade -= 1
            grenade_throw = False

        if player.in_air:
            player.revise_action(2)  # 2 - jump

        elif move_left or move_right:
            player.revise_action(1)  # 1- running
        else:
            player.revise_action(0)  # 0- idle

    # if player is dead
    else:
        player.revise_action(3)  # 3- death
        player.death = True

    player.draw(screen)
    player.update_animation()
    player.health_bar(10, 5, max_health, screen, 150, 20)


def draw_text(text, font, text_col, x, y):
    text_img = font.render(text, True, text_col)

    screen.blit(text_img, (x, y))


def player_speak():
    # display text
    dialog1_pos = (player.rect.x + 20, player.rect.y - 80)
    screen.blit(dialog1, dialog1_pos)
    draw_text(f"Stage : {level} Clear! {win_slogan[level]}", font1, RED,
              dialog1_pos[0] + 40, dialog1_pos[1] + 40)


def group_update():
    global game_lives

    # print(boss_group)

    # boss_group.update(screen, total_scroll, screen_scroll)

    bullet_group.draw(screen)
    bullet_group.update(player, enemy_group, bullet_group, tile.world_data, tanks_group)

    grenade_group.draw(screen)
    grenade_group.update(player, enemy_group, explosion_group, tanks_group, tile.world_data, screen_scroll)

    explosion_group.draw(screen)
    explosion_group.update(screen, screen_scroll)

    obstacle_group.draw(screen)  # killing group
    obstacle_group.update(screen, screen_scroll)

    tanks_group.draw(screen)
    tanks_group.update(screen_scroll)

    item_group.draw(screen)
    item_group.update(player, screen_scroll, item_group)


def draw_bg():
    screen.blit(bg_img[level], (0, 0))


def draw_win_screen():
    w_screen = pygame.image.load("background/new_scene/win-screen3.png").convert_alpha()
    win_screen = pygame.transform.scale(w_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(win_screen, (0, 0))


def clear_group():
    enemy_group.empty()
    bullet_group.empty()  # sprites matrix
    grenade_group.empty()
    explosion_group.empty()
    obstacle_group.empty()
    missile_group.empty()
    tanks_group.empty()
    item_group.empty()


def reset_game(music, last_score):
    global tile, level, move_left, move_right

    tile = Tile()
    tile.load_tiles(level, last_score)
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(0, 0.0, 10000)
    move_left = False
    move_right = False


# create instance for player
player = Gunner(player_x, player_y, "player", scale, 5, AMMON, GRENADE, max_health, last_score, timer)
# create instance for Tile
tile = Tile()
# load the tiles into the map
player = tile.load_tiles(level, last_score)  # go to level 2

# loading start up music
pygame.mixer.music.load("sound/start_music2.mp3")
pygame.mixer.music.play(0, 0.0, 10000)
pygame.mixer.music.set_volume(0.3)

# load images for buttons
new_game_img = pygame.image.load("button/new_game.png").convert_alpha()
exit_img = pygame.image.load("button/exit.png").convert_alpha()
help_img = pygame.image.load("button/help.png").convert_alpha()

# load start menu
menu_img = pygame.image.load("button/shoot-menu.png").convert_alpha()
start_menu = pygame.transform.scale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
help_menu_img = pygame.image.load("button/Help-menu.png").convert_alpha()
help_menu = pygame.transform.scale(help_menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

return_img = pygame.image.load("button/return.png").convert_alpha()
try_again_img = pygame.image.load("button/try_again.png").convert_alpha()

game_state = "menu"

# create instances for buttons
new_game_btn = Button(SCREEN_WIDTH // 3, 200, new_game_img, 0.5)
exit_btn = Button(SCREEN_WIDTH // 3, 300, exit_img, 0.5)
help_btn = Button(SCREEN_WIDTH // 2, 400, help_img, 0.1)
return_btn = Button(SCREEN_WIDTH // 3, 250, return_img, 0.3)
try_again_btn = Button(SCREEN_WIDTH // 3, 400, try_again_img, 0.3)

# Main Game Loop
while running:
    # check the game state

    # Menu State #
    if game_state == "menu":
        level = 0
        screen.fill(DARK_GREEN)
        screen.blit(start_menu, (0, 0))
        get_input()

        # run the game
        if new_game_btn.click(screen):
            game_state = "run"
            pygame.mixer.music.load("sound/game_music.mp3")
            pygame.mixer.music.play(0, 0.0, 10000)

        # create the help menu
        if help_btn.click(screen):
            game_state = "help"

        # exit the game
        if exit_btn.click(screen):
            pygame.quit()

    # Help state #
    elif game_state == "help":
        screen.fill(DARK_GREEN)
        screen.blit(help_menu, (0, 0))
        # getting input from user: when esc key is pressed, it would go back to the start menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"  # go back to main menu

    # Run State #
    elif game_state == "run":

        screen.fill((0, 180, 100))  # clear screen
        clock.tick(FPS)  # control frame rate
        draw_bg()  # draw game background
        draw_text(f"SCORE: {player.score}", font, "RED", SCREEN_WIDTH // 2, 20)  # show score

        # draw path
        # pygame.draw.lines(screen, "grey0", False, waypoints)
        timer.update()

        get_input()

        # check & update player status
        check_player_action()

        # Group position & animation update
        group_update()

        # Draw the tiles
        tile.draw_tiles(screen)

        print(player.rect.x)

        # enemy motion
        for enemy in enemy_group:
            enemy.ai(player, bullet_group, tile.world_data, screen_scroll)  # enemy move AI
            enemy.draw(screen)  # enemy redraw image
            enemy.update_animation()  # update new animation
            enemy.check_death(obstacle_group, tanks_group)
            enemy.health_bar(enemy.rect.x, enemy.rect.y - 10, 3, screen, 30, 5)  # max health is 3

            for tank in tanks_group:
                # check for tank & player position close enough and enemy with shooting capability
                rel_tank_player = tank.rect.centerx - player.rect.centerx
                tank.health_bar(tank.rect.x, tank.rect.y - 10, tank.init_health, screen, 30, 5)

                if tank.health <= 0:
                    tank.kill()
                    missile_group.empty()  # when tank killed, its missile needs to be eliminated too.
                # relative position between player and tank
                if tank.no_shoot is False and (400 > rel_tank_player > 0):  # shoot if within range
                    tank.shoot(missile_group)

                # drop bomb
                if tank.drop_bomb is True and (500 > rel_tank_player > -300):

                    if tank.bomb_counter < 2:  # initiate firing of bomb
                        if tank.img_index == 32:
                            bomb = Grenade(tank.rect.centerx, tank.rect.centery, 1, "missile")
                        else:
                            bomb = Grenade(tank.rect.centerx, tank.rect.centery, tank.direction, "bomb")
                        grenade_group.add(bomb)

                    if tank.bomb_counter > 500:
                        tank.bomb_counter = 0
                    tank.bomb_counter += 1

                # create an attribute drop bomb to the plane
                # create a condition for the plane to drop bomb
                # create an instance of bomb which belong to the class of grenade
                # use if statement to specify its specific move method
                # create a new method for dropping the bomb
                # within the bomb, create the explosion instance
                # collision detection condition

                missile_group.update(player, tank, screen_scroll, missile_group)

            missile_group.draw(screen)

        # check alive or not
        player.check_death(obstacle_group, tanks_group)

        draw_text(f"Grenade:{player.grenade}", font, ORANGE, 20, 30)
        draw_text(f"Bullets : {player.ammon}", font, ORANGE, 20, 50)

        if player.add_live:
            game_lives += 1
            player.add_live = False

        # Lose condition - Game over
        if player.death is True and game_lives > 0:
            player.dead_counter += 1
            if player.dead_counter > 50:
                screen_scroll = 0
                total_scroll = 0
                # reset the boss
                #boss.kill()
                #boss = Boss(boss_img, waypoints, 0)
                #boss_group.add(boss)

                pygame.mixer.music.stop()
                game_lives -= 1
                clear_group()
                last_score = player.score
                reset_game("sound/game_music.mp3", last_score)

        if game_lives <= 0:
            last_score = 0
            player.score = 0
            player.death = True
            if return_btn.click(screen):
                clear_group()
                level = 0
                reset_game("sound/start_music2.mp3", last_score)
                game_state = "menu"
                game_lives = 3

            # show up restart button, if restart button is clicked
            # set level back to 0
            # create a new instance of player, re-create tile class, load tile
            # empty group
            # if return to menu is clicked
            # return to menu

        # Win condition
        if player.win is True:

            if clear_to_count is False:
                count_time = pygame.time.get_ticks()
            clear_to_count = True

            player_speak()

            if pygame.time.get_ticks() - count_time > 3000:
                screen_scroll = 0
                total_scroll = 0
                clear_group()
                level += 1  # go up level
                if level > end_level:
                    game_state = "win"
                else:

                    movie = "movies/next-level.mp4"
                    Round_clear_movie(movie)

                    # screen reset
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

                    last_score = player.score
                    reset_game("sound/game_music.mp3", last_score)
                    clear_to_count = False

    # Win state #
    elif game_state == "win":
        last_score = 0
        draw_win_screen()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    level = 0
                    reset_game("sound/start_music2.mp3", last_score)
                    game_state = "menu"
                    game_lives = 3


    pygame.display.update()

    # print(f"last score: {last_score}")
    # print(f"player score: {player.score}")
pygame.quit()
