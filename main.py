import pygame
import math
import random
from settings import *
from sprites import SpriteSheet

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

bg_image = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
bg_image = pygame.transform.scale(bg_image, (WIN_WIDTH, WIN_HEIGHT))

# card = SpriteSheet('assets/deck_of_cards.png')
# x_margin = 11
# y_margin = 2
# x_pad = 22
# y_pad = 4

# card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)
# print(card_list)
# ace_hearts = card.image_at((11, 2, 43, 59))
########################################## SPRITE GROUPS ###############################################################

########################################################################################################################
cpa = SpriteSheet('assets/cpa_.png')
dr2a = SpriteSheet('assets/dr2a.png')
blue_knight_s = SpriteSheet('assets/BlueKnight.png')


stone_wall = cpa.image_at((0, 192, 64, 64))
stone_wall = pygame.transform.scale(stone_wall, (40, 40))

dark_stone_block = dr2a.image_at((5, 882, 128, 128), -1)
dark_stone_block = pygame.transform.scale(dark_stone_block, (40, 40))

knight_height = 50
blue_knight = blue_knight_s.image_at((42, 570, 39, 50), -1)
blue_knight = pygame.transform.flip(blue_knight, True, False)
clock = pygame.time.Clock()

running = True
########################################################################################################################

########################################################################################################################
# game loop
while running:
    # get all mouse, keyboard, controller events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(MIDNIGHT_BLUE)

    for j in range(4):
        for i in range(0, WIN_WIDTH//tile_size):
            screen.blit(stone_wall, (i * tile_size, WIN_HEIGHT - tile_size * j))

    for i in range(12):
        screen.blit(stone_wall, (0, tile_size * i))
    for i in range(12):
        screen.blit(stone_wall, (WIN_WIDTH - tile_size, tile_size * i))
    for i in range(1, 19):
        screen.blit(stone_wall, (tile_size * i, 0))

    screen.blit(dark_stone_block, (tile_size * 4, tile_size * 4))
    screen.blit(dark_stone_block, (tile_size * 5, tile_size * 5))
    screen.blit(dark_stone_block, (tile_size * 6, tile_size * 5))
    screen.blit(dark_stone_block, (tile_size * 6, tile_size * 11))
    screen.blit(dark_stone_block, (tile_size * 8, tile_size * 10))
    screen.blit(dark_stone_block, (tile_size * 9, tile_size * 9))
    screen.blit(dark_stone_block, (tile_size * 8, tile_size * 7))

    # for i in range(1, WIN_WIDTH // tile_size):
    #     pygame.draw.rect(screen, WHITE, (i*tile_size, 0, 3, WIN_HEIGHT))
    #
    # for j in range(1, WIN_HEIGHT // tile_size):
    #     pygame.draw.rect(screen, WHITE, (0, j*tile_size, WIN_WIDTH, 3))

    # screen.blit(dark_stone_block, (tile_size * 4, WIN_HEIGHT - tile_size * 4))
    screen.blit(blue_knight, (40, WIN_HEIGHT - tile_size * 4 - 10))
    pygame.display.flip()

    clock.tick(FPS)

# outside of game loop
pygame.quit()






























