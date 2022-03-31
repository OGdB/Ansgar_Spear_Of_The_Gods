import pygame
import pymunk


class Spear:
    def __init__(self, player_x, player_y, direction, spear_list, e_one, e_two):
        self.player_x = player_x
        self.player_y = player_y
        self.position = [player_x, player_y]
        self.direction = direction
        self.length = 32
        self.height = 16
        self.spear_list = spear_list
        self.lifetime = 100
        self.speed = 275
        self.spear_img = pygame.image.load("image\\Spear.png")
        self.rotated_spear = pygame.transform.rotate(self.spear_img, 180)
        self.enemy_one = e_one
        self.enemy_two = e_two

    def make_spear(self):
        new_spear = [self.position[0], self.position[1], self.direction, self.length, self.height, self.lifetime,
                     self.speed, self.direction]
        self.spear_list.append(new_spear)

    def update(self, dt):
        all_keys = pygame.key.get_pressed()
        for s in self.spear_list:
            s[5] -= dt * 10

            if s[2] == "left":
                s[0] -= s[6] * dt
            else:
                s[0] += s[6] * dt
            if s[0] <= 0:
                s[6] = 0
            if s[0] >= 480 - s[3]:
                s[6] = 0
            if s[5] <= 0:
                self.spear_list.remove(s)

            hit_check = self.enemy_one.enemy_hit_check(s[0], s[1], s[1] + s[4], 100)
            if hit_check:
                self.spear_list.remove(s)
            hit_check = self.enemy_two.enemy_hit_check(s[0], s[1], s[1] + s[4], 100)
            if hit_check:
                self.spear_list.remove(s)

        if all_keys[pygame.K_a] or all_keys[pygame.K_LEFT]:
            self.direction = "left"
            if all_keys[pygame.K_LSHIFT]:
                self.position[0] -= 250 * dt  # this will let Ansgar run
            else:
                self.position[0] -= 150 * dt

        if all_keys[pygame.K_d] or all_keys[pygame.K_RIGHT]:
            self.direction = "right"
            if all_keys[pygame.K_LSHIFT]:
                self.position[0] += 250 * dt
            else:
                self.position[0] += 150 * dt

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
        self.shape = pymunk.Poly(self.body, poly_dims)
        self.shape.friction = 0.25
        space.add(self.body, self.shape)

        self.direction = "right"
        spear_list = []

        self.s = Spear(self.body.position.x, self.body.position.y, self.direction, spear_list, e_one, e_two)

    def draw(self, surf):
        self.body.angle = 0
        # position of drawing vertices is body position + dimensions.
        # got to do something regarding rotations as well (on collision)

        top_left = (self.body.position.x - self.dim_radius, self.body.position.y - self.dim_radius)
        top_right = (self.body.position.x + self.dim_radius, self.body.position.y - self.dim_radius)
        bottom_left = (self.body.position.x - self.dim_radius, self.body.position.y + self.dim_radius)
        bottom_right = (self.body.position.x + self.dim_radius, self.body.position.y + self.dim_radius)

        pygame.draw.polygon(surf, (255, 255, 0), [top_left, top_right, bottom_right, bottom_left])

    def update(self, dt, evt, keys):
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

        #     if self.jump == False:
        #
        #         self.ansgar_v_speed += 10 * dt
        #         if self.ansgar_v_speed >= 20 or self.position[1] <= 250:
        #             self.jump = True
        #             self.ansgar_v_speed *= -1
        #
        #     self.ansgar_accel += self.ansgar_v_speed
        #     self.position[1] -= self.ansgar_accel * dt
        #     self.s.position[1] -= self.ansgar_accel * dt
        #     if self.ansgar_accel > self.ansgar_max_speed:
        #         self.ansgar_accel = -self.ansgar_max_speed
        #         self.s.position[1] = -self.ansgar_max_speed
        #     if self.position[1] >= 290:
        #         self.position[1] = 290
        #         self.s.position[1] = 290
        #         self.jump = False
        # else:
        #     self.ansgar_d_speed = 100000 * dt
        #     self.ansgar_accel = 0
        #     self.ansgar_v_speed = 0
        #
        #     # Decelerate
        #
        #     if self.position[1] < 290:
        #         self.position[1] += self.ansgar_d_speed * dt
        #         self.s.position[1] += self.ansgar_d_speed * dt
        #         if self.position[1] >= 290:
        #             self.position[1] = 290
        #             self.s.position[1] = 290
        #             self.jump = False
        #
        # if all_keys[pygame.K_a] or all_keys[pygame.K_LEFT]:
        #     if all_keys[pygame.K_LSHIFT]:
        #         # this will let Ansgar run
        #         self.position[0] -= 250 * dt
        #     else:
        #         self.position[0] -= 150 * dt
        #     self.direction = "left"
        # if all_keys[pygame.K_d] or all_keys[pygame.K_RIGHT]:
        #     if all_keys[pygame.K_LSHIFT]:
        #         # this will let Ansgar run
        #         self.position[0] += 250 * dt
        #     else:
        #         self.position[0] += 150 * dt
        #     self.direction = "right"
        # if self.position[0] <= 0:
        #     self.position[0] = 0
        # if self.position[0] >= 480 - 32:
        #     self.position[0] = 480 - 32
        #
        # if evt.type == pygame.KEYDOWN:
        #     if evt.key == pygame.K_SPACE:
        #         self.s.make_spear()
        # self.s.update(dt)
