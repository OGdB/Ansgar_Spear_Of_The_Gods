import random
import pygame.draw
import Classes


def draw_all_arrows(arrow_list, surf):
    for cur_box in arrow_list:
        x = cur_box[0]
        y = cur_box[1]
        size = cur_box[2]
        color = cur_box[3]
        pygame.draw.rect(surf, color, (x, y, size, size))


def spawn_new_arrow(arrow_list, enemy_x, enemy_y, enemy_length):
    size = 5
    x = enemy_x + enemy_length
    y = enemy_y + (enemy_length / 2)
    color = (150, 150, 150)
    speed = 100

    new_box = [x, y, size, color, speed]
    arrow_list.append(new_box)


class Enemy_Spawner:
    dim = 0

    def __init__(self, starting_x, starting_y, type):
        self.Red = random.randint(0, 255)
        self.Blue = random.randint(0, 255)
        self.Green = random.randint(0, 255)
        self.x = starting_x
        self.y = starting_y
        # self.vertical_speed = random.randint(0, 100)  # pixels / second
        self.color = (self.Red, self.Blue,
                      self.Green)
        self.health = Classes.health.Health()
        self.rect = pygame.Rect(self.x, self.y, self.dim, self.dim)
        self.dead = False
        self.arrow_list = []
        if type == 1:  # A Melee enemy
            self.horizontal_speed = random.randint(50, 100)  # pixels / second
            self.type = "melee"
            self.flipped = True
        elif type == 2:  # A shooting enemy
            self.horizontal_speed = random.randint(10, 50)  # pixels / second
            self.type = "range"
            self.flipped = True
            self.cooldown = 0
            self.shoot = 30

    def update(self, dt, left_x_border, right_x_border, hero_x, hero_y, screen_h):
        # self.vertical_speed += 100 * dt
        # self.horizontal_speed += 100 * dt

        self.x += self.horizontal_speed * dt
        self.rect = pygame.Rect(self.x, self.y, self.dim, self.dim)
        # self.y += self.vertical_speed * dt

        # Move towards the hero
        if self.type == "melee":
            distance_x = abs(hero_x - self.x)
            distance_y = abs(hero_y - self.y)
            if distance_x <= 30 and distance_y <= 16:
                if self.x > hero_x:
                    self.horizontal_speed = -(abs(self.horizontal_speed))
                elif self.x < hero_x:
                    self.horizontal_speed = abs(self.horizontal_speed)

        # Will stand still and shoot at the hero
        if self.type == "range":
            distance_x = abs(hero_x - self.x)
            distance_y = abs(hero_y - self.y)
            if distance_x <= 200 and distance_y <= 16:
                if self.x > hero_x:
                    self.horizontal_speed = (abs(self.horizontal_speed))
                    if self.shoot == self.cooldown:
                        spawn_new_arrow(self.arrow_list, self.x, self.y, self.dim)
                        self.cooldown = 5
                    else:
                        self.cooldown += 1
                elif self.x < hero_x:
                    self.horizontal_speed = -(abs(self.horizontal_speed))
                    if self.shoot == self.cooldown:
                        spawn_new_arrow(self.arrow_list, self.x, self.y, self.dim)
                        self.cooldown = 0
                    else:
                        self.cooldown += 1
            for a in self.arrow_list:
                a[0] += a[4] * dt

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
        if self.x <= s_x <= self.x + self.dim and s_y_t <= self.y <= s_y_b:
            return True
        else:
            return False

    def enemy_attack_check(self, hero_r):
        if self.type == "melee":
            if hero_r.colliderect(self.rect):
                return 25
            else:
                return 0
        if self.type == "range":
            for i in range(len(self.arrow_list)):
                temp_rect = (self.arrow_list[i][0], self.arrow_list[i][1], self.arrow_list[i][2], self.arrow_list[i][2])
                if hero_r.colliderect(temp_rect):
                    return 50
            return 0

    def draw(self, surf, img):
        if self.flipped:
            flipped_img = pygame.transform.flip(img, True, False)
            surf.blit(flipped_img, (self.x, self.y))
        else:
            surf.blit(img, (self.x, self.y))
        health_bar = self.health.cur_health / self.health.max_health
        health_bar_w = health_bar * 20
        pygame.draw.rect(surf, (255, 0, 0), (self.x - 2, self.y - 7, health_bar_w, 5))
        pygame.draw.rect(surf, (255, 0, 255),
                         self.rect, 1)
        if self.type == "range":
            draw_all_arrows(self.arrow_list, surf)
