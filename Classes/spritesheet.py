import math
import pygame


class SpriteSheet:
    """Deals with getting portions of spritesheets"""
    def __init__(self, image, tile_width, tile_height, columns):
        self.sheet = image
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.columns = columns

    def get_x(self, frame):
        frame = (frame % self.columns)  # get the remainder of frame / columns as a tile
        return frame * 16

    def get_sprite(self, frame):
        """return a specific sprite from sprite sheet"""
        sprite = pygame.Surface((self.tile_width, self.tile_height)).convert_alpha()
        sprite.set_colorkey((0, 0, 0))
        x = self.get_x(frame)
        y = math.floor(frame/self.columns) * 16
        sprite.blit(self.sheet, (0, 0), (x, y, self.tile_width, self.tile_height))
        return sprite

    def load_animation(self, start_frame, amount_of_frames):
        """return an animation from a sprite sheet starting at frame 0"""
        animation = []
        current_frame = start_frame

        for x in range(amount_of_frames):
            animation.append(self.get_sprite(current_frame))
            current_frame += 1
        return animation

    def flip_sprite(self, hor, ver):
        self.sheet = pygame.transform.flip(self.sheet, hor, ver)
        self.sheet.set_colorkey((0, 0, 0))
        return self.sheet
