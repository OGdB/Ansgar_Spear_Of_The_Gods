import random

import pygame.draw

import Classes


class Enemy_Spawner:

    dim = 0

    def __init__(self, starting_x, starting_y, type):
        self.Red = random.randint(0, 255)
        self.Blue = random.randint(0, 255)
        self.Green = random.randint(0, 255)
        self.x = starting_x
        self.y = starting_y
        self.horizontal_speed = random.randint(50, 100)  # pixels / second
        # self.vertical_speed = random.randint(0, 100)  # pixels / second
        self.color = (self.Red, self.Blue,
                      self.Green)
        self.health = Classes.health.Health()
        self.dead = False
        self.flipped = True
        if type == 1:  # A Melee enemy
            self.type = "melee"
        elif type == 2:  # A shooting enemy
            self.type = "range"

    def update(self, dt, left_x_border, right_x_border, hero_x, hero_y, screen_h):
        # self.vertical_speed += 100 * dt
        # self.horizontal_speed += 100 * dt

        self.x += self.horizontal_speed * dt
        # self.y += self.vertical_speed * dt
        if self.type == "melee":
            distance_x = abs(hero_x - self.x)
            distance_y = abs(hero_y - self.y)

            if distance_x <= 30 and distance_y <= 16:
                if self.x > hero_x:
                    self.horizontal_speed = -(abs(self.horizontal_speed))
                elif self.x < hero_x:
                    self.horizontal_speed = abs(self.horizontal_speed)
                #Move towards the hero
            if self.x < left_x_border:
                # We just went off the left-edge
                self.x = left_x_border
                self.horizontal_speed *= -1
                self.flipped = not self.flipped
            if self.x > right_x_border - Enemy_Spawner.dim:
                # We just went off the right-edge
                self.x = right_x_border - Enemy_Spawner.dim
                self.horizontal_speed *= -1
                self.flipped = not self.flipped

        if self.x < left_x_border:
            # We just went off the left-edge
            self.x = left_x_border
            self.horizontal_speed *= -1
            self.flipped = not self.flipped
        if self.x > right_x_border - Enemy_Spawner.dim:
            # We just went off the right-edge
            self.x = right_x_border - Enemy_Spawner.dim
            self.horizontal_speed *= -1
            self.flipped = not self.flipped

        # if self.y < Enemy_Spawner.dim:
            # We just went off the top-edge
        #    self.y = Enemy_Spawner.dim
        #    self.vertical_speed *= -1
        # if self.y > screen_h - Enemy_Spawner.dim:
            # We just went off the bottom-edge
        #    self.y = screen_h - Enemy_Spawner.dim
        #    self.vertical_speed *= -1

    def enemy_hit_check(self, s_x, s_y_t, s_y_b):
        if self.x <= s_x <= self.x+self.dim and s_y_t <= self.y <= s_y_b:
            return True
        else:
            return False

    def draw(self, surf, img):
        if self.flipped:
            flipped_img = pygame.transform.flip(img, True, False)
            surf.blit(flipped_img, (self.x, self.y))
        else:
            surf.blit(img, (self.x, self.y))
        health_bar = self.health.cur_health / self.health.max_health
        health_bar_w = health_bar * 20
        pygame.draw.rect(surf, (255, 0, 0), (self.x - 2, self.y - 7, health_bar_w, 5))
        # pygame.draw.rect(surf, self.color, (self.x, self.y, Enemy_Spawner.dim, Enemy_Spawner.dim))
