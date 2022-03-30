import pygame
from settings import *
import math

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
        left and switch.  Same reasoning for y. Calls self.images_at() to get a
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
    def __init__(self, x, y, tiles, enemies=None):
        if enemies is None:
            enemies = []
        self.tiles = tiles
        # self.tiles, self.enemy_list = Level.get_layout(self)
        blue_knight_s = SpriteSheet('assets/BlueKnight.png')
        self.standl = blue_knight_s.image_at((42, 570, 39, 50), -1)
        self.standr = pygame.transform.flip(self.standl, True, False)
        self.blue_knight_run_l = blue_knight_s.load_strip((41, 385, 48, 48), 10, -1)
        self.blue_knight_run_r = [pygame.transform.flip(player, True, False) for player in self.blue_knight_run_l]
        #################### ATTACK ####################
        self.attack_left = []
        self.blue_lattack1 = blue_knight_s.image_at((60, 159, 42, 50), -1)
        self.attack_left.append(self.blue_lattack1)

        self.blue_lattack2 = blue_knight_s.image_at((116, 159, 47, 52), -1)
        self.attack_left.append(self.blue_lattack2)

        self.blue_lattack3 = blue_knight_s.image_at((173, 156, 54, 50), -1)
        self.attack_left.append(self.blue_lattack3)

        self.blue_lattack4 = blue_knight_s.image_at((235, 149, 48, 58), -1)
        self.attack_left.append(self.blue_lattack4)

        self.blue_lattack5 = blue_knight_s.image_at((292, 160, 52, 46), -1)
        self.attack_left.append(self.blue_lattack5)

        self.blue_lattack6 = blue_knight_s.image_at((347, 159, 60, 50), -1)
        self.attack_left.append(self.blue_lattack6)

        self.blue_lattack7 = blue_knight_s.image_at((414, 162, 55, 46), -1)
        self.attack_left.append(self.blue_lattack7)

        self.blue_lattack8 = blue_knight_s.image_at((486, 159, 42, 49), -1)
        self.attack_left.append(self.blue_lattack8)

        self.blue_lattack9 = blue_knight_s.image_at((550, 160, 38, 48), -1)
        self.attack_left.append(self.blue_lattack9)

        self.blue_lattack10 = blue_knight_s.image_at((611, 160, 41, 50), -1)
        self.attack_left.append(self.blue_lattack10)

        self.attack_right = [pygame.transform.flip(item, True, False) for item in self.attack_left]
        ################################################
        self.y_velo = 0
        self.x_velo = 0
        self.right = False
        self.left = False
        self.last = pygame.time.get_ticks()
        self.last_a = pygame.time.get_ticks()
        self.image_delay = 100
        self.attack_delay = 75
        self.current_frame = 0
        self.current_attack = 0
        self.image = self.standr
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.jumping = False
        self.falling = False
        self.deltay = 0
        self.tile_speed = 0
        self.tile_right = False
        self.tile_left = False
        self.attacks = False
        self.enemy_list = enemies

    def draw(self, display):
        # draws the player to the display
        display.blit(self.image, (self.image_rect.x, self.image_rect.y))
        pygame.draw.rect(display, WHITE, self.image_rect, 2)

    def attack(self):
        now = pygame.time.get_ticks()
        if self.right or self.image == self.standr or self.image in self.attack_right:
            if now - self.last >= self.attack_delay:
                self.last = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_right)
                self.image = self.attack_right[self.current_frame]
                self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y)
                for tile in self.tiles:
                    if self.image_rect.colliderect(tile[1].x, tile[1].y, tile[1].width, tile[1].height):
                        self.attack = False
                        self.image = self.standr
                        self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y)
                        self.x_velo = 0
        elif self.left or self.image == self.standl or self.image in self.attack_left:
            if now - self.last >= self.attack_delay:
                self.last = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_left)
                self.image = self.attack_left[self.current_frame]
                self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y)

    def update(self):
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            now = pygame.time.get_ticks()
            self.right = True
            self.left = False
            dx = 2
            if now - self.last >= self.image_delay:
                self.last = now
                self.current_frame = (self.current_frame + 1) % len(self.blue_knight_run_r)
                self.image = self.blue_knight_run_r[self.current_frame]
                self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y, w=39, h=50)
        elif keys[pygame.K_LEFT]:
            now = pygame.time.get_ticks()
            self.right = False
            self.left = True
            dx = -2
            if now - self.last_a >= self.image_delay:
                self.last_a = now
                self.current_attack = (self.current_attack + 1) % len(self.blue_knight_run_l)
                self.image = self.blue_knight_run_l[self.current_attack]
                self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y, w=39, h=50)
        else:
            dx = 0
            if self.right:
                self.image = self.standr
                self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y)
            elif self.left:
                self.image = self.standl
                self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y)
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

        if keys[pygame.K_SPACE]:
            self.attacks = True
            Player.attack(self)
        else:
            if self.image in self.attack_left:
                self.image = self.standl
                self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y)
            elif self.image in self.attack_right:
                self.image = self.standr
                self.image_rect = self.image.get_rect(x=self.image_rect.x, y=self.image_rect.y)
            self.attacks = False

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

            keys = pygame.key.get_pressed()
            # switch camera
            if self.image_rect.x + dx >= WIDTH - WIDTH / 3:
                dx = 0
                self.tile_speed = -2
                self.tile_right = True
            elif not keys[pygame.K_RIGHT] and not self.tile_left:
                self.tile_speed = 0
                self.tile_right = False
            if self.tile_right:
                if self.image_rect.colliderect(tile[1].x + self.tile_speed, tile[1].y, tile[1].width, tile[1].height):
                    dx = 0
                    self.tile_speed = 0
            # left camera
            if self.image_rect.x + dx <= 100:
                dx = 0
                self.tile_speed = 2
                self.tile_left = True
            elif not keys[pygame.K_LEFT] and not self.tile_right:
                self.tile_speed = 0
                self.tile_left = False
            if self.tile_left:
                if self.image_rect.colliderect(tile[1].x + self.tile_speed, tile[1].y, tile[1].width, tile[1].height):
                    dx = 0
                    self.tile_speed = 0

        for tile in self.tiles:
            tile[1].x += self.tile_speed

        self.x_velo = dx
        self.deltay = dy
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
        red_knight_s = SpriteSheet('assets/RedKnight.png')
        red_standl = red_knight_s.image_at((42, 570, 39, 50), -1)
        self.tile_speed = 2
        self.layout = level_layout
        self.tile_size = tile_size
        self.tile_list = []
        self.player_list = []
        self.enemy_list = []
        self.enemy_rects = []
        self.collided = False

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
                    self.player = Player(x_val, y_val, self.tile_list)
                    # self.player_list.append(self.player)
                elif col == 'e':
                    enemy = Enemies(x_val, y_val, self.tile_list)
                    self.enemy_list.append(enemy)
                elif col == 'd':
                    img_rect = wood_door.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (wood_door, img_rect)
                    self.tile_list.append(tile)

    def get_layout(self):
        return self.tile_list

    def get_enemies(self):
        return self.enemy_list

    def draw(self, display):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])
        # for player in self.player_list:
        self.player.draw(display)
        for enemy in self.enemy_list:
            enemy.draw(display)

    def update(self, display):
        # for player in self.player_list:
        self.player.update()
        for enemy in self.enemy_list:
            enemy.update()
            if self.player.tile_right:
                enemy.image_rect.x += -2
            elif self.player.tile_left:
                enemy.image_rect.x += 2
            if enemy.image_rect.colliderect(self.player.image_rect.x,
                                            self.player.image_rect.y,
                                            self.player.image_rect.width,
                                            self.player.image_rect.height):
                if self.player.attacks:
                    self.enemy_list.remove(enemy)
                else:
                    self.collided = True
        if self.collided:
            self.__init__(self.layout, self.tile_size)
            self.collided = False


class Spikes:
    def __init__(self, x, y, tile_size, tiles):
        self.tiles_size = tile_size
        self.tiles = tiles


class Enemies:
    def __init__(self, x, y, tile_list):
        self.tile_list = tile_list
        red_knight_s = SpriteSheet('assets/RedKnight.png')
        self.standl = red_knight_s.image_at((42, 570, 39, 50), -1)
        self.standr = pygame.transform.flip(self.standl, True, False)
        self.red_knight_run_l = red_knight_s.load_strip((41, 385, 48, 48), 10, -1)
        self.red_knight_run_r = [pygame.transform.flip(enemy, True, False) for enemy in self.red_knight_run_l]
        self.image = self.standl
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.y_velo = 0
        self.deltay = 0
        self.x_velo = 0
        self.last = pygame.time.get_ticks()
        self.run_distance = 1200
        self.switch = 1
        self.right = False
        self.left = False
        self.delay_run = 75
        self.last_run = pygame.time.get_ticks()
        self.image_numb = 0

    def draw(self, display):
        display.blit(self.image, (self.image_rect.x, self.image_rect.y))
        pygame.draw.rect(display, WHITE, self.image_rect, 2)

    def update(self):
        dx = 0
        dy = 0
        for tile in self.tile_list:
            if self.image_rect.colliderect(tile[1].x, tile[1].y, tile[1].width, tile[1].height):
                dx = abs(self.image_rect.x - tile[1].x)
                dy = -2
        self.image_rect.x += dx
        self.image_rect.y += dy
        now = pygame.time.get_ticks()
        if now - self.last >= self.run_distance:
            self.switch *= -1
            self.last = now
        if self.switch > 0:
            dx = 2
            self.right = True
            self.left = False
        else:
            dx = -2
            self.right = False
            self.left = True
        if self.right:
            self.image = self.red_knight_run_r[self.image_numb]
            now = pygame.time.get_ticks()
            if now - self.delay_run >= self.last_run:
                self.last_run = now
                self.image_numb += 1
                if self.image_numb >= len(self.red_knight_run_r):
                    self.image_numb = 0
        elif self.left:
            self.image = self.red_knight_run_l[self.image_numb]
            now = pygame.time.get_ticks()
            if now - self.delay_run >= self.last_run:
                self.last_run = now
                self.image_numb += 1
                if self.image_numb >= len(self.red_knight_run_l):
                    self.image_numb = 0

        self.x_velo = dx
        self.deltay = dy
        self.image_rect.x += dx
        self.image_rect.y += dy



