import pygame
import math
import random
from settings import *
from sprites import Level

pygame.init()
# colors in RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
COLORS = [RED, GREEN, BLUE, BLACK]

# Math Constants
PI = math.pi

# Game Constants
SIZE = (WIN_WIDTH, WIN_HEIGHT)
FPS = 60

##############################################################################
##############################################################################

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Animation Intro')

# bg_image = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# bg_image = pygame.transform.scale(bg_image, (WIN_WIDTH, WIN_HEIGHT))

########################################## SPRITE GROUPS ###############################################################

########################################################################################################################
clock = pygame.time.Clock()

running = True
########################################################################################################################
level1 = Level(LAYOUT1, tile_size)
layout_list = level1.get_layout()
bg_image = pygame.image.load('assets/Dungeon.jpg')
########################################################################################################################
# game loop
while running:
    # get all mouse, keyboard, controller events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_image, (0, 0))
    level1.draw(screen)
    level1.update()

    pygame.display.flip()

    clock.tick(FPS)

# outside of game loop
pygame.quit()
