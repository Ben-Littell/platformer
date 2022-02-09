import pygame
from settings import *

# This class handles sprite sheets
# https://www.pygame.org/wiki/Spritesheet
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        """rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
                         y_margin=0, y_padding=0, width=None, height=None, colorkey=None):
        """Load a grid of images.
        x_margin is the space between the top of the sheet and top of the first
        row. x_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for y. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.
        if width and height:
            x_sprite_size = width
            y_sprite_size = height
        else:
            x_sprite_size = (sheet_width - 2 * x_margin
                             - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                             - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)
        return self.images_at(sprite_rects, colorkey)


class Player:
    def __init__(self, x, y, tile_size, tiles):
        self.tile_size = tile_size
        self.tiles = tiles
        blue_knight_s = SpriteSheet('assets/BlueKnight.png')
        self.standl = blue_knight_s.image_at((42, 570, 39, 50), -1)
        self.standr = pygame.transform.flip(self.standl, True, False)
        self.blue_knight_run_l = blue_knight_s.load_strip((41, 385, 48, 48), 10, -1)
        self.blue_knight_run_r = [pygame.transform.flip(player, True, False) for player in self.blue_knight_run_l]
        self.y_velo = 0
        self.x_velo = 0
        self.right = False
        self.left = False
        self.last = pygame.time.get_ticks()
        self.image_delay = 100
        self.current_frame = 0
        self.image = self.standr
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.jumping = False
        self.falling = False

    def draw(self, display):
        display.blit(self.image, (self.image_rect.x, self.image_rect.y))
        pygame.draw.rect(display, WHITE, self.image_rect, 2)

    def update(self):
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            now = pygame.time.get_ticks()
            self.right = True
            self.left = False
            dx = 2
            if now - self.last >= self.image_delay:
                self.last = now
                self.current_frame = (self.current_frame + 1) % len(self.blue_knight_run_r)
                self.image = self.blue_knight_run_r[self.current_frame]
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            now = pygame.time.get_ticks()
            self.right = False
            self.left = True
            dx = -2
            if now - self.last >= self.image_delay:
                self.last = now
                self.current_frame = (self.current_frame + 1) % len(self.blue_knight_run_l)
                self.image = self.blue_knight_run_l[self.current_frame]
        else:
            dx = 0
            if self.right:
                self.image = self.standr
            elif self.left:
                self.image = self.standl
            self.right = False
            self.left = False
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.jumping and not self.falling:
            self.y_velo = -15
            self.jumping = True
        dy += self.y_velo
        self.y_velo += 1
        if self.y_velo < 0:
            self.jumping = True
            self.falling = False
        else:
            self.jumping = False
            self.falling = True

        for tile in self.tiles:
            if tile[1].colliderect(dx + self.image_rect.x, self.image_rect.y,
                                   self.image_rect.width, self.image_rect.height):
                dx = 0
            if tile[1].colliderect(self.image_rect.x, self.image_rect.y + dy,
                                   self.image_rect.width, self.image_rect.height):
                if self.y_velo < 0:
                    dy = tile[1].bottom - self.image_rect.top
                    self.y_velo = 0
                    self.jumping = False
                    self.falling = True
                elif self.y_velo > 0:
                    dy = tile[1].top - self.image_rect.bottom
                    self.y_velo = 0
                    self.falling = False
                    self.jumping = False

        self.image_rect.x += dx
        self.image_rect.y += dy


class Level:
    def __init__(self, level_layout, tile_size):
        cpa = SpriteSheet('assets/cpa_.png')
        dr2a = SpriteSheet('assets/dr2a.png')
        stone_wall = cpa.image_at((0, 192, 64, 64))
        stone_wall = pygame.transform.scale(stone_wall, (tile_size, tile_size))
        wood_door = cpa.image_at((194, 385, 58, 126))
        wood_door = pygame.transform.scale(wood_door, (tile_size, tile_size * 2))
        dark_stone_block = dr2a.image_at((5, 882, 128, 128), -1)
        dark_stone_block = pygame.transform.scale(dark_stone_block, (tile_size, tile_size))

        self.tile_list = []
        self.player_list = []

        for i, row in enumerate(level_layout):
            for j, col in enumerate(row):
                x_val = j * tile_size
                y_val = i * tile_size

                if col == "1":
                    img_rect = stone_wall.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (stone_wall, img_rect)
                    self.tile_list.append(tile)
                elif col == "2":
                    img_rect = dark_stone_block.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (dark_stone_block, img_rect)
                    self.tile_list.append(tile)
                elif col == 'p':
                    player = Player(x_val, y_val, tile_size, self.tile_list)
                    self.player_list.append(player)

    def draw(self, display):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])
        for player in self.player_list:
            player.update()
            player.draw(display)

    def get_layout(self):
        return self.tile_list


class Spikes:
    def __init__(self, x, y, tile_size, tiles):
        self.tiles_size = tile_size
        self.tiles = tiles


class Enemies:
    def __init__(self):
        pass
