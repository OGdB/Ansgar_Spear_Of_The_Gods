import pygame
import pymunk
import Classes.map_data
import Classes.health
import Classes.spritesheet as SpriteSheet

class Spear:
    def __init__(self, player_x, player_y, direction, spear_list, e_list, cam_pos):
        self.position = [player_x, player_y]
        self.direction = direction
        self.length = 32
        self.height = 16
        self.spear_list = spear_list
        self.lifetime = 100
        self.speed = 275
        self.e_list = e_list
        self.spear_img = pygame.image.load("image\\Spear.png")
        self.rotated_spear = pygame.transform.rotate(self.spear_img, 180)
        self.cam_pos = cam_pos
        self.walled = False

    def update(self, dt):
        all_keys = pygame.key.get_pressed()
        for s in self.spear_list:
            s[5] -= dt * 10

            if not self.walled:
                if s[2] == "left":
                    s[0] -= s[6] * dt
                else:
                    s[0] += s[6] * dt

            if s[5] <= 0:
                self.spear_list.remove(s)

            for i in range(len(self.e_list)):
                hit_check = self.e_list[i].enemy_hit_check(s[0], s[1], s[1] + s[4], 50)
                if hit_check:
                    self.spear_list.remove(s)

        if all_keys[pygame.K_a] or all_keys[pygame.K_LEFT]:
            self.direction = "left"

        if all_keys[pygame.K_d] or all_keys[pygame.K_RIGHT]:
            self.direction = "right"

    def draw(self, surf):
        for new_spear in self.spear_list:
            if new_spear[7] == "right":
                surf.blit(self.spear_img, (new_spear[0] - self.cam_pos[0], new_spear[1] - self.cam_pos[1]))
            else:
                surf.blit(self.rotated_spear, (new_spear[0] - self.cam_pos[0], new_spear[1] - self.cam_pos[1]))


class Ansgar:
    def __init__(self, pos, space, enemy_list, cam_pos):
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
        self.e_list = enemy_list
        self.map = Classes.map_data.Map("maps\\Map.json")
        self.points = self.map.floor_points
        self.grounded = False
        self.handler = space.add_default_collision_handler()
        self.cam_pos = cam_pos
        self.s = Spear(self.body.position.x, self.body.position.y, self.direction, self.spear_list, self.e_list, self.cam_pos)
        # Animation attributes
        self.anim_timer = 0
        self.anim_frame = 0
        char_spr_sheet_img = pygame.image.load("image\\Ansgar_Spritesheet.png").convert_alpha()
        char_spr_sheet = SpriteSheet.SpriteSheet(char_spr_sheet_img, 32, 32, 4)
        self.idle_right = char_spr_sheet.load_animation(0, 4)
        self.walk_right = char_spr_sheet.load_animation(4, 4)
        self.idle_left = char_spr_sheet.load_animation(8, 4)
        self.walk_left = char_spr_sheet.load_animation(12, 4)
        self.cur_anim = self.idle_right
        self.anim_cooldown = 0.2
        self.health_bar = self.health.cur_health / self.health.max_health

    def make_spear(self):
        # this should make it to where ansgar looks like he's throwing the spear
        new_spear = [self.body.position[0], (self.body.position[1] - 15), self.direction, self.length, self.height,
                     self.lifetime,
                     self.speed, self.direction]
        self.spear_list.append(new_spear)

    def draw(self, surf, cam_pos, dt):
        # Ansgar Animation loop
        self.anim_timer += dt
        if self.anim_timer >= self.anim_cooldown:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % len(self.cur_anim)
        cur_sprite = self.cur_anim[self.anim_frame]
        cur_sprite.set_colorkey((0, 0, 0))

        self.body.angle = 0

        surf.blit(cur_sprite, (self.body.position.x - self.dim_radius - cam_pos[0], self.body.position.y - self.dim_radius - cam_pos[1]))

        self.health_bar = self.health.cur_health / self.health.max_health
        health_bar_w = self.health_bar * self.dim_radius * 2
        pygame.draw.rect(surf, (255, 0, 0),
                         ((self.body.position.x - self.dim_radius + 1) - self.cam_pos[0], (self.body.position.y - self.dim_radius - 7) - self.cam_pos[1],
                          health_bar_w, 5))

        self.s.draw(surf)

    def coll_begin(self, arbiter, space, data):

        self.grounded = True
        return True

    def coll_pre(self, arbiter, space, data):
        self.grounded = True
        return True

    def coll_post(self, arbiter, space, data):


        return True

    def separate(self, arbiter, space, data):

        self.grounded = False

    def update(self, dt, evt, keys):
        self.rect = pygame.Rect(
            self.body.position.x - self.dim_radius, self.body.position.y - self.dim_radius,
            self.dim_radius * 2, self.dim_radius * 2)

        for i in range(len(self.e_list)):
            dmg, force, direction = self.e_list[i].enemy_attack_check(self.rect)
            if dmg > 0:

                self.health.take_damage(dmg)
            if force > 0:
                if direction:
                    # Should send player to the right
                    self.body.apply_impulse_at_local_point((force, 0), (0, 0))
                else:
                    # Should send the player to the left
                    self.body.apply_impulse_at_local_point((-force, 0), (0, 0))


        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_w:

            if self.grounded == True:
                self.grounded = False
                self.body.apply_impulse_at_local_point((0, -700), (0, 8))

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not keys[pygame.K_d] and not keys[pygame.K_RIGHT]:
            self.direction = "left"
            self.cur_anim = self.walk_left
            if keys[pygame.K_LSHIFT]:
                # this will let Ansgar run

                self.body.force = (-800, 0)
            else:
                self.body.force = (-1000, 0)

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not keys[pygame.K_a] and not keys[pygame.K_LEFT]:
            self.direction = "right"
            self.cur_anim = self.walk_right
            if keys[pygame.K_LSHIFT]:
                # this will let Ansgar run
                self.body.force = (800, 0)
            else:
                self.body.force = (1000, 0)

        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
            self.make_spear()
        self.s.update(dt)

        if evt.type == pygame.KEYUP:
            if (evt.key == pygame.K_a or evt.key == pygame.K_LEFT) and self.direction == "left":
                self.cur_anim = self.idle_left
            if (evt.key == pygame.K_d or evt.key == pygame.K_RIGHT) and self.direction == "right":
                self.cur_anim = self.idle_right

        self.limit_velocity(self.body)

        self.handler.begin = self.coll_begin
        self.handler.pre_solve = self.coll_pre
        self.handler.post_solve = self.coll_post
        self.handler.separate = self.separate
        if self.handler.begin == True:
            self.grounded = True

    def limit_velocity(self, body):
        vel_limit = 150

        if abs(body.velocity.x) > vel_limit:
            import math
            dir_sign = math.copysign(1, body.velocity.x)
            limited_vel = (dir_sign * 150, body.velocity.y)
            body.velocity = limited_vel
