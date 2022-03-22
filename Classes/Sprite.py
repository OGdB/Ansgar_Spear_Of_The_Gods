import pygame

class Sprite(pygame.sprite.Sprite):  # Platform class is Sprite Class with extra attributes
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((50, 205, 50))
        self.rect = self.image.get_rect()  # Get a rect with the sizes of the image.
        self.rect.x = x
        self.rect.y = y

    def draw(self, win):
        pygame.draw.rect(win, (50, 205, 50), self.rect, self.rect.width)
