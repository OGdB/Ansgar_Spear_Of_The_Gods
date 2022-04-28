import random
import pygame.draw
import Classes
import Classes.spritesheet


def spawn_new_arrow(arrow_list, enemy_x, enemy_y, enemy_length, speed):
    size = 5
    x = enemy_x + enemy_length
    y = enemy_y + (enemy_length / 2)
    color = (150, 150, 150)

    new_box = [x, y, size, color, speed]
    arrow_list.append(new_box)


class Enemy_Spawner:

    def __init__(self, starting_x, starting_y, dim, type):
        self.Red = random.randint(0, 255)
        self.Blue = random.randint(0, 255)
        self.Green = random.randint(0, 255)
        # self.vertical_speed = random.randint(0, 100)  # pixels / second
        self.color = (self.Red, self.Blue,
                      self.Green)
        self.health = Classes.health.Health()
        self.rect = 0
        #self.rect = pygame.Rect(self.x, self.y, self.sfactor * self.dim, self.sfactor * self.dim)
        self.dead = False
        self.flipped = True
        self.anim_timer = 0
        self.anim_frame = 0
        self.anim_cooldown = 0.2

        if type == 1:  # A Melee enemy
            bear_animation_sheet = pygame.image.load("image\\Bear_Spritesheet.png")
            bear_animation = Classes.spritesheet.SpriteSheet(bear_animation_sheet, 32, 16, 2)
            self.walk_right = bear_animation.load_animation(0, 2)
            self.walk_left = bear_animation.load_animation(2, 2)
            self.horizontal_speed = random.randint(50, 100)  # pixels / second
            self.sfactor = 1
            self.damage = .5
            self.dim = self.sfactor * dim
            self.x = starting_x - self.dim
            self.y = starting_y - self.dim
            self.type = "melee"
        elif type == 2:  # A shooting enemy
            fire_bear_animation_sheet = pygame.image.load("image\\Fire_Bear_Spritesheet.png")
            fire_bear_animation = Classes.spritesheet.SpriteSheet(fire_bear_animation_sheet, 32, 16, 2)
            self.walk_right = fire_bear_animation.load_animation(0, 2)
            self.walk_left = fire_bear_animation.load_animation(2, 2)
            self.horizontal_speed = random.randint(10, 50)  # pixels / second
            self.sfactor = 1
            self.damage = 1
            self.dim = self.sfactor * dim
            self.x = starting_x - self.dim
            self.y = starting_y - self.dim
            self.type = "range"
            self.cooldown = 0
            self.shoot = 30
        elif type == 3:
            self.sfactor = 3
            tank_bear_animation_sheet = pygame.image.load("image\\BearArmor_Spritesheet.png")
            new_w = int(tank_bear_animation_sheet.get_width() * self.sfactor)
            new_h = int(tank_bear_animation_sheet.get_height() * self.sfactor)
            new_tank_bear = pygame.transform.scale(tank_bear_animation_sheet, (new_w, new_h))
            tank_bear_animation = Classes.spritesheet.SpriteSheet(new_tank_bear, 32 * self.sfactor, 16 * self.sfactor, 2)
            self.walk_right = tank_bear_animation.load_animation(0, 2)
            self.walk_left = tank_bear_animation.load_animation(2, 2)
            self.horizontal_speed = random.randint(5, 10)  # pixels / second
            self.original_speed = self.horizontal_speed
            self.dim = self.sfactor * dim
            self.damage = 10
            self.x = starting_x - self.dim
            self.y = starting_y - self.dim
            self.chase_speed = 50
            self.type = "tank"

    def update(self, dt, left_x_border, right_x_border, hero_x, hero_y, arrow_list, screen_h):
        # self.vertical_speed += 100 * dt
        # self.horizontal_speed += 100 * dt

        self.x += self.horizontal_speed * dt
        self.rect = pygame.Rect(self.x, self.y, self.dim * 2, self.dim)
        self.sfactor = self.sfactor
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
                fired_x = self.x
                fired_y = self.y
                enemy_dim = self.dim
                if self.x > hero_x:
                    self.horizontal_speed = (abs(self.horizontal_speed))
                    if self.shoot == self.cooldown:
                        spawn_new_arrow(arrow_list, fired_x, fired_y, enemy_dim, -100)
                        self.cooldown = 5
                    else:
                        self.cooldown += 1
                elif self.x < hero_x:
                    self.horizontal_speed = -(abs(self.horizontal_speed))
                    if self.shoot == self.cooldown:
                        spawn_new_arrow(arrow_list, fired_x, fired_y, enemy_dim, 100)
                        self.cooldown = 0
                    else:
                        self.cooldown += 1

        if self.type == "tank":
            self.sfactor += .5
            if self.sfactor >= 4:
                self.sfactor = 4
            distance_x = abs(hero_x - self.x)
            distance_y = abs(hero_y - self.y) + 5
            if distance_x <= 60 and distance_y <= 36:
                if self.x > hero_x:
                    self.horizontal_speed = -(abs(self.chase_speed))
                elif self.x < hero_x:
                    self.horizontal_speed = abs(self.chase_speed)
            else:
                if self.horizontal_speed < 0:
                    self.horizontal_speed = -(abs(self.original_speed))
                else:
                    self.horizontal_speed = abs(self.original_speed)

        if self.x < left_x_border:
            # We just went off the left-edge
            self.x = left_x_border
            self.horizontal_speed *= -1
            self.flipped = not self.flipped
        elif self.x > right_x_border - self.dim * 2:
            # We just went off the right-edge
            self.x = right_x_border - self.dim * 2
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
            if self.type == "tank":
                return True, (self.health.cur_health/self.sfactor)
            else:
                return True, 0
        else:
            return False, 0

    def enemy_attack_check(self, hero_r, arrow_list):
        if self.type == "melee":
            if hero_r.colliderect(self.rect):
                return self.damage, 100, self.flipped
            else:
                return 0, 0, 0
        elif self.type == "range":
            for arrow in arrow_list:
                temp_rect = (arrow[0], arrow[1], arrow[2], arrow[2])
                if hero_r.colliderect(temp_rect):
                    return self.damage, 5, self.flipped
            return 0, 0, 0
        elif self.type == "tank":
            if hero_r.colliderect(self.rect):
                return self.damage, 200, self.flipped
            else:
                return 0, 0, 0

    def draw(self, surf, dt, cam_pos):
        self.anim_timer += dt
        if self.flipped:
            if self.anim_timer >= self.anim_cooldown:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(self.walk_left)
            cur_sprite = self.walk_left[self.anim_frame]
            cur_sprite.set_colorkey((0, 0, 0))
            surf.blit(cur_sprite, (self.x - cam_pos[0], self.y - cam_pos[1]))
        else:
            if self.anim_timer >= self.anim_cooldown:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(self.walk_right)
            cur_sprite = self.walk_right[self.anim_frame]
            cur_sprite.set_colorkey((0, 0, 0))
            surf.blit(cur_sprite, (self.x - cam_pos[0], self.y - cam_pos[1]))

        health_bar = self.health.cur_health / self.health.max_health
        health_bar_w = health_bar * 20
        pygame.draw.rect(surf, (255, 0, 0), ((self.x - 2) - cam_pos[0], (self.y - 7) - cam_pos[1], health_bar_w, 5))
        pygame.draw.rect(surf, (255, 0, 255), self.rect, 1)
