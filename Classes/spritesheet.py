import math
import pygame

class SpriteSheet:
    """Deals with getting portions of spritesheets"""
    def __init__(self, image):
        self.sheet = image

    def get_x(self, frame, columns):
        frame = (frame % columns)  # get the remainder of frame / columns as a tile
        return frame * 16

    def get_sprite(self, frame, tile_width, tile_height, columns):
        """return a specific sprite from sprite sheet"""
        sprite = pygame.Surface((tile_width, tile_height)).convert_alpha()
        sprite.set_colorkey((0, 0, 0))
        x = self.get_x(frame, columns)
        y = math.floor(frame/columns) * 16
        sprite.blit(self.sheet, (0, 0), (x, y, tile_width, tile_height))
        return sprite

    def load_animation(self, start_frame, amount_of_frames):
        """return an animation from a sprite sheet starting at start_frame for specified amount of frames"""
        animation = []
        current_frame = start_frame

        for x in range(amount_of_frames):
            animation.append(self.get_sprite(current_frame, 64, 64, (0, 0, 0)))
            current_frame += 1
        return animation

    def flip_sprite(self, hor, ver):
        self.sheet = pygame.transform.flip(self.sheet, hor, ver)
        self.sheet.set_colorkey((0, 0, 0))
        return self.sheet
