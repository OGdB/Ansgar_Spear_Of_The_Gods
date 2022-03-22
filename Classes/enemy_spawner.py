import random
import pygame


class Enemy_Spawner:

    dim = 0

    def __init__(self, starting_x, starting_y, health):
        self.Red = random.randint(0, 255)
        self.Blue = random.randint(0, 255)
        self.Green = random.randint(0, 255)
        self.x = starting_x
        self.y = starting_y
        self.horizontal_speed = random.randint(50, 100)  # pixels / second
        # self.vertical_speed = random.randint(0, 100)  # pixels / second
        self.color = (self.Red, self.Blue,
                      self.Green)
        self.health = health
        self.dead = False

    def update(self, dt, left_x_border, right_x_border, screen_h):
        # self.vertical_speed += 100 * dt
        # self.horizontal_speed += 100 * dt
        # self.life_time -= 50 * dt

        self.x += self.horizontal_speed * dt
        # self.y += self.vertical_speed * dt

        if self.x < left_x_border:
            # We just went off the left-edge
            self.x = left_x_border
            self.horizontal_speed *= -1
        if self.x > right_x_border - Enemy_Spawner.dim:
            # We just went off the right-edge
            self.x = right_x_border - Enemy_Spawner.dim
            self.horizontal_speed *= -1

        # if self.y < Enemy_Spawner.dim:
            # We just went off the top-edge
        #    self.y = Enemy_Spawner.dim
        #    self.vertical_speed *= -1
        # if self.y > screen_h - Enemy_Spawner.dim:
            # We just went off the bottom-edge
        #    self.y = screen_h - Enemy_Spawner.dim
        #    self.vertical_speed *= -1

    def enemy_hit_check(self, m_x, m_y):
        if self.x <= m_x <= self.x+self.dim and self.y <= m_y <= self.y+self.dim:
            return True
        else:
            return False

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, (self.x, self.y, Enemy_Spawner.dim, Enemy_Spawner.dim))