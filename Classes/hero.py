import pygame
import pymunk
import Classes.health


class Spear:
    def __init__(self, player_x, player_y, direction, spear_list, e_one, e_two):
        self.player_x = player_x
        self.player_y = player_y
        self.position = [self.player_x, self.player_y]
        self.direction = direction
        self.length = 32
        self.height = 16
        self.spear_list = spear_list
        self.lifetime = 100
        self.speed = 275
        self.enemy_one = e_one
        self.enemy_two = e_two
        self.spear_img = pygame.image.load("image\\temp_spear.png")
        self.rotated_spear = pygame.transform.rotate(self.spear_img, 180)

    def update(self, dt):
        all_keys = pygame.key.get_pressed()
        for s in self.spear_list:
            s[5] -= dt * 10

            if s[2] == "left":
                s[0] -= s[6] * dt
            else:
                s[0] += s[6] * dt

            if s[5] <= 0:
                self.spear_list.remove(s)

            hit_check = self.enemy_one.enemy_hit_check(s[0], s[1], s[1] + s[4], 50)
            if hit_check:
                self.spear_list.remove(s)
            hit_check = self.enemy_two.enemy_hit_check(s[0], s[1], s[1] + s[4], 50)
            if hit_check:
                self.spear_list.remove(s)

        if all_keys[pygame.K_a] or all_keys[pygame.K_LEFT]:
            self.direction = "left"

        if all_keys[pygame.K_d] or all_keys[pygame.K_RIGHT]:
            self.direction = "right"

    def draw(self, surf):
        for new_spear in self.spear_list:
            if new_spear[7] == "right":
                surf.blit(self.spear_img, (new_spear[0], new_spear[1]))
                pygame.draw.rect(surf, (100, 100, 100), (new_spear[0], new_spear[1], new_spear[3], new_spear[4]), 1)
            else:
                surf.blit(self.rotated_spear, (new_spear[0], new_spear[1]))


class Ansgar:
    def __init__(self, pos, space, e_one, e_two):
        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.body.angle = 0
        self.body.mass = 5
        self.dim_radius = 15
        poly_dims = [(-self.dim_radius, -self.dim_radius), (self.dim_radius, -self.dim_radius),
                     (self.dim_radius, self.dim_radius), (-self.dim_radius, self.dim_radius)]
        self.rect = pygame.Rect(
            self.body.position.x - self.dim_radius, self.body.position.y - self.dim_radius,
            self.dim_radius * 2, self.dim_radius * 2)
        self.shape = pymunk.Poly(self.body, poly_dims)
        self.shape.friction = 0.25
        space.add(self.body, self.shape)
        self.length = 32
        self.height = 16
        self.lifetime = 100
        self.speed = 275
        self.direction = "right"
        self.spear_list = []
        self.health = Classes.health.Health()
        self.e_one = e_one
        self.e_two = e_two

        self.s = Spear(self.body.position.x, self.body.position.y, self.direction, self.spear_list, e_one, e_two)

    def make_spear(self):
        # this should make it to where ansgar looks like he's throwing the spear
        new_spear = [self.body.position[0], self.body.position[1] - 15, self.direction, self.length, self.height,
                     self.lifetime,
                     self.speed, self.direction]
        self.spear_list.append(new_spear)

    def draw(self, surf):
        self.body.angle = 0
        # position of drawing vertices is body position + dimensions.
        # got to do something regarding rotations as well (on collision)

        top_left = (self.body.position.x - self.dim_radius, self.body.position.y - self.dim_radius)
        top_right = (self.body.position.x + self.dim_radius, self.body.position.y - self.dim_radius)
        bottom_left = (self.body.position.x - self.dim_radius, self.body.position.y + self.dim_radius)
        bottom_right = (self.body.position.x + self.dim_radius, self.body.position.y + self.dim_radius)

        pygame.draw.polygon(surf, (255, 255, 0), [top_left, top_right, bottom_right, bottom_left])

        health_bar = self.health.cur_health / self.health.max_health
        health_bar_w = health_bar * self.dim_radius * 2
        pygame.draw.rect(surf, (255, 0, 0),
                         (self.body.position.x - self.dim_radius + 1, self.body.position.y - self.dim_radius - 7,
                          health_bar_w, 5))
        pygame.draw.rect(surf, (255, 0, 255),
                         self.rect, 1)

        self.s.draw(surf)

    def update(self, dt, evt, keys):
        self.rect = pygame.Rect(
            self.body.position.x - self.dim_radius, self.body.position.y - self.dim_radius,
            self.dim_radius * 2, self.dim_radius * 2)
        dmg = self.e_one.enemy_attack_check(self.rect)
        if dmg > 0:
            self.health.take_damage(dmg)
        dmg = self.e_two.enemy_attack_check(self.rect)
        if dmg > 0:
            self.health.take_damage(dmg)

        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_w:
            self.body.apply_impulse_at_local_point((0, -700), (0, 8))

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if keys[pygame.K_LSHIFT]:
                # this will let Ansgar run

                self.body.force = (-800, 0)
            else:
                self.body.force = (-1000, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_LSHIFT]:
                # this will let Ansgar run
                self.body.force = (800, 0)
            else:
                self.body.force = (1000, 0)



        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = "right"

        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_SPACE:
                self.make_spear()
        self.s.update(dt)
