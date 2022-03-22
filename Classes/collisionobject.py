import pygame
import Classes.Sprite as Sprite

#platforms = pygame.sprite.Group()
WHITE = (255,255,255)
BLACK = (0  ,0  ,0  )
RED   = (255,0  ,0  )
GREEN = (0  ,255,0  )
BLUE  = (0  ,0  ,255)
class CollisionObject(Sprite.Sprite):  # Platform class is Sprite Class with extra attributes
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        Sprite.Sprite.__init__(self, x, y, w, h)
        self.collision = [False] * 9

    def check_collision(self, other_rect):
        self.collision[0] = other_rect.collidepoint(self.rect.topleft)
        self.collision[1] = other_rect.collidepoint(self.rect.topright)
        self.collision[2] = other_rect.collidepoint(self.rect.bottomleft)
        self.collision[3] = other_rect.collidepoint(self.rect.bottomright)

        self.collision[4] = other_rect.collidepoint(self.rect.midleft)
        self.collision[5] = other_rect.collidepoint(self.rect.midright)
        self.collision[6] = other_rect.collidepoint(self.rect.midtop)
        self.collision[7] = other_rect.collidepoint(self.rect.midbottom)

        self.collision[8] = other_rect.collidepoint(self.rect.center)

    def draw_collision(self, screen):
        # TOP AND BOTTOM
        self.draw_point(screen, self.rect.topleft, self.collision[0])
        self.draw_point(screen, self.rect.topright, self.collision[1])
        self.draw_point(screen, self.rect.bottomleft, self.collision[2])
        self.draw_point(screen, self.rect.bottomright, self.collision[3])

        # LEFT AND RIGHT
        self.draw_point(screen, self.rect.midleft, self.collision[4])
        self.draw_point(screen, self.rect.midright, self.collision[5])
        self.draw_point(screen, self.rect.midtop, self.collision[6])
        self.draw_point(screen, self.rect.midbottom, self.collision[7])

        # CENTER
        self.draw_point(screen, self.rect.center, self.collision[8])

    def draw_point(self, screen, pos, collision):
        if not collision:
            pygame.draw.circle(screen, GREEN, pos, 5)
        else:
            pygame.draw.circle(screen, RED, pos, 5)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
