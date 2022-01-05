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

card = SpriteSheet('assets/deck_of_cards.png')
x_margin = 11
y_margin = 2
x_pad = 22
y_pad = 4

# card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)
# print(card_list)
ace_hearts = card.image_at((11, 2, 43, 59))


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

    screen.fill(BLUE)
    for i in range(1, WIN_WIDTH // tile_size):
        pygame.draw.rect(screen, WHITE, (i*tile_size, 0, 3, WIN_HEIGHT))

    for j in range(1, WIN_HEIGHT // tile_size):
        pygame.draw.rect(screen, WHITE, (0, j*tile_size, WIN_WIDTH, 3))

    screen.blit(ace_hearts, (100, 100))
    pygame.display.flip()

    clock.tick(FPS)

# outside of game loop
pygame.quit()


