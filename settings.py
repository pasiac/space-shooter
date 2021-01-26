import pygame
WIDTH = 1000
HEIGHT = 1000
FPS = 60

#game constants
player_vel = 20
player_width = 150
player_health = 3
asteroid_width = 100
asteroid_kill_count = 0
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

#defining colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)

#loading sprites
background = pygame.transform.scale(pygame.image.load('space_background.gif'), (WIDTH, HEIGHT)) 
player_img = pygame.transform.scale(pygame.image.load('player_ship.png'), (player_width, player_width))
asteroid_img = pygame.transform.scale(pygame.image.load('asteroid.png'), (asteroid_width, asteroid_width))
big_asteroid_img = pygame.transform.scale(pygame.image.load('asteroid.png'), (asteroid_width*2, asteroid_width*2))
laser = pygame.transform.scale(pygame.image.load('laser.png'), (laser_width, laser_height))

alien_1 = pygame.transform.scale(pygame.image.load('alien_1.png'), (alien_width, alien_width))
alien_2 = pygame.transform.scale(pygame.image.load('alien_2.png'), (alien_width, alien_width))
alien_sprites = [alien_1, alien_2]

boss_image = pygame.transform.scale(pygame.image.load('alien_boss.png'), (boss_width, boss_height))