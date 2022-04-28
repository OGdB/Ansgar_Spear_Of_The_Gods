import pygame
import pymunk
import Classes.map_data
import Classes.health
import Classes.spritesheet as SpriteSheet


class Spear:
    def __init__(self, player_pos, direction, spc, handler):
        length = 32
        self.height = 16
        self.lifetime = 100
        speed = 275


        self.spear_img = pygame.image.load("image\\Spear.png")
        if direction == "left":
            self.spear_img = pygame.transform.rotate(self.spear_img, 180)

        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.KINEMATIC)
        self.body.angle = 0
        dimensions = [(0, 0), (length, 0), (length, self.height), (0, self.height)]  # pivot top-left
        self.shape = pymunk.Poly(self.body, dimensions)
        self.body.position = (player_pos.x, player_pos.y - 8)
        self.shape.collision_type = 1
        handler.begin = self.spear_platform_coll

        if direction == "left":
            self.body.velocity = (-speed, 0)
        else:
            self.body.velocity = (speed, 0)

        spc.add(self.body, self.shape)

    def spear_platform_coll(self, arbiter, space, data):
        self.body.velocity = (0, 0)
        self.shape.collision_type = 10 # Make different collision type so that the player can now collide with the spear
        return True

    def update(self, dt, enemies_list, spear_list, space):
        self.lifetime -= dt * 10  # lifetime deterioration
        for i in range(len(enemies_list)):  # hit detection with enemies
            hit_check = enemies_list[i].enemy_hit_check(self.body.position.x, self.body.position.y,
                                                        self.body.position.y + self.height, 50)

            if self.lifetime <= 0 or hit_check:  # lifetime out or hitting enemy -> remove spear
                space.remove(self.body, self.shape)
                spear_list.remove(self)
                del self
                return

    def draw(self, surf):
        surf.blit(self.spear_img, self.body.position)


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
        self.shape.collision_type = 2
        self.shape.friction = 0.25
        self.space = space
        space.add(self.body, self.shape)
        self.length = 32
        self.height = 16
        self.lifetime = 100
        self.speed = 800
        self.run_speed = 1000
        self.direction = "right"
        self.spear_list = []
        self.health = Classes.health.Health()
        self.e_list = enemy_list
        self.map = Classes.map_data.Map("maps\\Map.json")
        self.points = self.map.floor_points
        self.grounded = False
        self.handler = space.add_collision_handler(0, 2)  # Collision between ground collision type (0, and Ansgar (2)
        self.counter = 0
        self.cam_pos = cam_pos
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

        self.spear_wildcard_col_handler = space.add_wildcard_collision_handler(1)
        self.spear_wildcard_col_handler.begin = self.spear_any_coll
        self.spear_platform_col_handler = space.add_collision_handler(0, 1)



    def make_spear(self):
        # this should make it to where ansgar looks like he's throwing the spear
        if self.counter <= 0:
            self.counter = 1.5
            spear = Spear(self.body.position, self.direction, self.space, self.spear_platform_col_handler)
            self.spear_list.append(spear)

    def spear_any_coll(self, arbiter, space, data):
        return False  # Ignore collisions with anything but the platforms (in the next function).

    def draw(self, surf, cam_pos, dt):
        # Ansgar Animation loop
        self.anim_timer += dt
        if self.anim_timer >= self.anim_cooldown:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % len(self.cur_anim)
        cur_sprite = self.cur_anim[self.anim_frame]
        cur_sprite.set_colorkey((0, 0, 0))

        self.body.angle = 0

        surf.blit(cur_sprite, (
            self.body.position.x - self.dim_radius - cam_pos[0], self.body.position.y - self.dim_radius - cam_pos[1]))

        self.health_bar = self.health.cur_health / self.health.max_health
        health_bar_w = self.health_bar * self.dim_radius * 2
        pygame.draw.rect(surf, (255, 0, 0),
                         ((self.body.position.x - self.dim_radius + 1) - self.cam_pos[0],
                          (self.body.position.y - self.dim_radius - 7) - self.cam_pos[1],
                          health_bar_w, 5))

        for spear in self.spear_list:
            spear.draw(surf)

    def coll_begin(self, arbiter, space, data):
        self.grounded = True
        return True

    def coll_pre(self, arbiter, space, data):
        self.grounded = True
        return True

    def separate(self, arbiter, space, data):

        self.grounded = False

    def update(self, dt, evt, keys):
        self.counter -= dt

        self.rect = pygame.Rect(
            self.body.position.x - self.dim_radius, self.body.position.y - self.dim_radius, self.dim_radius * 2,
            self.dim_radius * 2)

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

        
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_w or evt.key == pygame.K_UP:

                if evt.type == pygame.KEYDOWN and evt.key == pygame.K_w:

                    if self.grounded == True:
                        self.grounded = False
                        self.body.apply_impulse_at_local_point((0, -700), (0, 8))
                if self.grounded == True:
                    self.grounded = False
                    self.body.apply_impulse_at_local_point((0, -700), (0, 8))

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not keys[pygame.K_d] and not keys[pygame.K_RIGHT]:
            self.direction = "left"
            self.cur_anim = self.walk_left
            if keys[pygame.K_LSHIFT]:
                # this will let Ansgar run

                self.body.force = (-self.run_speed, 0)
            else:
                self.body.force = (-self.speed, 0)

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not keys[pygame.K_a] and not keys[pygame.K_LEFT]:
            self.direction = "right"
            self.cur_anim = self.walk_right
            if keys[pygame.K_LSHIFT]:
                # this will let Ansgar run
                self.body.force = (self.run_speed, 0)
            else:
                self.body.force = (self.speed, 0)

        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
            self.make_spear()

        for spear in self.spear_list:
            spear.update(dt, self.e_list, self.spear_list, self.space)

        if evt.type == pygame.KEYUP:
            if (evt.key == pygame.K_a or evt.key == pygame.K_LEFT) and self.direction == "left":
                self.cur_anim = self.idle_left
            if (evt.key == pygame.K_d or evt.key == pygame.K_RIGHT) and self.direction == "right":
                self.cur_anim = self.idle_right

        self.limit_velocity(self.body)

        self.handler.begin = self.coll_begin
        self.handler.pre_solve = self.coll_pre
        self.handler.separate = self.separate

    def limit_velocity(self, body):
        vel_limit = 150

        if abs(body.velocity.x) > vel_limit:
            import math
            dir_sign = math.copysign(1, body.velocity.x)
            limited_vel = (dir_sign * 150, body.velocity.y)
            body.velocity = limited_vel
