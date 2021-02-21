# import pygame
import random
import os
import pygame

SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(SETTINGS_DIR, "statics")


def load_scaled_image(filename, width, height):
    return pygame.transform.scale(pygame.image.load(f"{STATIC_DIR}/sprites/{filename}"), (width, height))


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FPS = 60

PLAYER_VELOCITY = 20
player_width = 150
player_health = 3
asteroid_width = 100
scrolling_speed = 5
big_asteroid_health = 5
laser_width = 50
laser_height = 80
laser_vel = 20
enemy_laser_width = 10
enemy_laser_height = 70
laser_delay = 10
aliens = []
lasers = []
laser_count = 0
alien_width = 200
alien_health = 5
alien_vel = 4
boss_width = 700
boss_height = 250
bosses = []
boss_vel = 3
boss_health = 150
boss_spawned = False
boss_death_count = 0

count = 0
alien_frame_count = 0

# defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# loading sprites
background = load_scaled_image("space_background.gif", WINDOW_WIDTH, WINDOW_HEIGHT)
player_img = load_scaled_image('player_ship.png', player_width, player_width)
asteroid_img = load_scaled_image('asteroid.png', asteroid_width, asteroid_width)
big_asteroid_img = load_scaled_image('asteroid.png', asteroid_width*2, asteroid_width*2)
laser_img = load_scaled_image('laser.png', laser_width, laser_height)
alien_1 = load_scaled_image('alien_1.png', alien_width, alien_width)
alien_2 = load_scaled_image('alien_2.png', alien_width, alien_width)
alien_sprites = [alien_1, alien_2]
boss_image = load_scaled_image('alien_boss.png', boss_width, boss_height)


DEFAULT_ASTEROID_RECT_CENTER = (random.randrange(0, WINDOW_WIDTH - 100), 0)
DEFAULT_PLAYER_RECT_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.1)


