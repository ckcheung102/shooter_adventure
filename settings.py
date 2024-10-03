import pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

# color settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BLACK = (0, 0, 0)
DARK_GREEN = (0, 180, 100)
RED = (255, 0, 0)
ORANGE = (255, 30, 80)
PINK = (255, 100, 120)
YELLOW = (200, 255, 0)

# define player settings:
player_x = 100
player_y = 100
player_speed = 4
scale = 1.0

enemy_x = 500
enemy_y = 200

num_enemy = 1

AMMON = 20
GRENADE = 5

TILE_SIZE = 32

scroll_range = 200
screen_scroll = 0

# background
bg_num = 7
bg_scroll = 0

max_health = 6  # player/enemy health
num_image = 40  # no. of images or characters in the game

win_slogan = [

    " Oh yes, I pass my test",
    "Yoyo, I'm gonna get going",
    "Now, winner is me ! ",
    "It's so easy, I'll be a winner",
    "I like another challenge",
    "Just complete my quest",
    "My life goes on Yeah ! ",
    "My quests finished! "

]
