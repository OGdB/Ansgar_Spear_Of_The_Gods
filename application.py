import math
import sys

import pygame
import pymunk
import Classes.map_data
import Classes.enemy
import Classes.hero
import Classes.health
import Death_screen


# Set to true to see a bunch of debug stuff.
debug = False

class Application:
    def __init__(self, screen_w, screen_h, port_w, port_h):
        pygame.init()
        self.win = pygame.display.set_mode((int(port_w), int(port_h)), pygame.FULLSCREEN)  # The main window
        self.half_port_w = port_w / 2  # half-window width in pixels
        self.half_port_h = port_h / 2  # half-window height in pixels
        self.camera_pos = pygame.Vector2(0, 0)  # The position (in world-space) of the camera.  Will be updated in update
        self.done = False  # Should we bail out of the game loop?
        self.clock = pygame.time.Clock()  # The pygame clock object used for delta-time
        self.font = pygame.font.SysFont("Courier New", 16)  # The font to use for rendering stats

        self.background = pygame.image.load("image\\Background.png")
        self.background = pygame.transform.scale(self.background, (screen_w, screen_h))


        self.space = pymunk.Space()  # Create a physics space
        self.space.gravity = (0, 250)  # Set its gravity

        self.cur_map = Classes.map_data.Map("maps\\Map.json")  # The initial map to load
        self.total_time = 0  # Total time the game's been running (used for player/coin color modulation)
        self.ground_colliders = self.cur_map.draw_colliders(self.space)
        self.enemy_group_list = [
            # Melee Bears
            # Classes.enemy.EnemyGroups(x, y, amount of bears, size, right border, type, camera_pos),
            Classes.enemy.EnemyGroups(336, 240, 3, 16, 672, 1, self.camera_pos),
            Classes.enemy.EnemyGroups(128, 480, 3, 16, 464, 1, self.camera_pos),
            Classes.enemy.EnemyGroups(848, 672, 3, 16, 1040, 1, self.camera_pos),
            Classes.enemy.EnemyGroups(192, 704, 3, 16, 272, 1, self.camera_pos),
            Classes.enemy.EnemyGroups(416, 848, 3, 16, 576, 1, self.camera_pos),
            Classes.enemy.EnemyGroups(927, 272, 3, 16, 1024, 1, self.camera_pos),
            Classes.enemy.EnemyGroups(1440, 192, 3, 16, 1552, 1, self.camera_pos),
            # Range Bears
            Classes.enemy.EnemyGroups(0, 128, 2, 16, 80, 2, self.camera_pos),
            Classes.enemy.EnemyGroups(528, 448, 2, 16, 624, 2, self.camera_pos),
            Classes.enemy.EnemyGroups(1184, 480, 2, 16, 1456, 2, self.camera_pos),
            # Tank Bears
            Classes.enemy.EnemyGroups(832, 896, 1, 16, 1072, 3, self.camera_pos),
            Classes.enemy.EnemyGroups(1216, 753, 1, 16, 1360, 3, self.camera_pos),

        ]
        self.ansgar = Classes.hero.Ansgar((240, 100), self.space, self.enemy_group_list,self.camera_pos)
        self.player_health = self.ansgar.health_bar
        pygame.mixer.music.load('rock.mp3')
        pygame.mixer.music.play(-1)
        self.paused = False

    def run(self):
        while not self.done:
            self.delta_time = self.clock.tick(60) / 1000
            self.space.step(self.delta_time)
            self.camera_position()
            self.handle_input(self.delta_time)
            self.render(self.win, self.delta_time)
            self.player_health = self.ansgar.health_bar



        # Shut down pygame after we're done with our game loop (because the program is likely to shut down shortly after)


    def handle_input(self, dt):
        # Process the event (make sure this is only once in your game loop!)
        evt = pygame.event.poll()
        if self.paused == False:
            for i in range(len(self.enemy_group_list)):
                self.enemy_group_list[i].update(dt, self.ansgar.body.position.x, self.ansgar.body.position.y)

        # event-handling
        all_keys = pygame.key.get_pressed()

        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if evt.key == pygame.K_F11:
                global debug
                debug = not debug
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_p:
                if self.paused == False:
                    self.paused = True
                else:
                    self.paused = False
        if self.paused == False:
            self.ansgar.update(dt, evt, all_keys)
        else:
            self.delta_time = 0
            
        if self.player_health == 0:
            self.done = True





    def camera_position(self):
        self.camera_pos.x = self.ansgar.body.position.x - self.half_port_w  # camera x pos at top-left of width
        self.camera_pos.y = self.ansgar.body.position.y - self.half_port_h

        if self.camera_pos.x < 0:
            self.camera_pos.x = 0
        if self.camera_pos.x > self.cur_map.world_width - self.win.get_width():
            self.camera_pos.x = self.cur_map.world_width - self.win.get_width()
        if self.camera_pos.y < 0:
            self.camera_pos.y = 0
        if self.camera_pos.y > self.cur_map.world_height - self.win.get_height():
            self.camera_pos.y = self.cur_map.world_height - self.win.get_height()

    def render(self, surf, dt):
        # Drawing
        surf.fill((0, 0, 0))
        surf.blit(self.background, (0, 0))

        surf.blit(self.cur_map.rendered_img, (0, 0),
                  (self.camera_pos.x, self.camera_pos.y, self.win.get_width(), self.win.get_height()))

        for i in range(len(self.enemy_group_list)):
            self.enemy_group_list[i].draw(self.win, dt)

        # Debug drawing
        if debug:
            for platform_points in self.cur_map.floor_points:
                pygame.draw.line(surf, (255, 255, 0),
                                 (platform_points[0] - self.camera_pos.x, platform_points[2] - self.camera_pos.y),
                                 (platform_points[1] - self.camera_pos.x, platform_points[2] - self.camera_pos.y))
                pygame.draw.line(surf, (255, 255, 0),
                                 (platform_points[0] - self.camera_pos.x, platform_points[2] - self.camera_pos.y + 16),
                                 (platform_points[1] - self.camera_pos.x, platform_points[2] - self.camera_pos.y + 16))
                # sides
                pygame.draw.line(surf, (255, 255, 0),
                                 (platform_points[0] - self.camera_pos.x, platform_points[2] - self.camera_pos.y),
                                 (platform_points[0] - self.camera_pos.x, platform_points[2] - self.camera_pos.y + 16))
                pygame.draw.line(surf, (255, 255, 0),
                                 (platform_points[1] - self.camera_pos.x, platform_points[2] - self.camera_pos.y),
                                 (platform_points[1] - self.camera_pos.x, platform_points[2] - self.camera_pos.y + 16))

            # Draw red dot on start_x of colliders
            for platform_points in self.cur_map.floor_points:
                start_x = platform_points[0] - self.camera_pos.x
                end_x = platform_points[1] - self.camera_pos.x
                y = platform_points[2] - self.camera_pos.y
                pygame.draw.circle(surf, (255, 0, 0), [start_x, y], 3)
                pygame.draw.circle(surf, (255, 255, 0), [end_x, y], 3)
            cam_pos_text = f"[{math.floor(self.camera_pos[0])}, {math.floor(self.camera_pos[1])}]"

            # Debug text telling you which tile-row and column is hovered over with the mouse
            # MousePos
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x = math.floor((mouse_x + self.camera_pos[0]) / self.cur_map.tile_width % self.cur_map.map_width) * 16
            y = math.floor((mouse_y + self.camera_pos[1]) / self.cur_map.tile_height % self.cur_map.map_height) * 16
            mouse_pos_text = f"[{x}, {y}]"

            # Velocity
            player_vel_text = f"[{math.floor(self.ansgar.body.velocity.x)}, {math.floor(self.ansgar.body.velocity.y)}]"

            white = (255, 255, 255)
            font = pygame.font.Font('freesansbold.ttf', 32)
            mouse_text_render = font.render(mouse_pos_text, True, white)
            cam_pos_render = font.render(cam_pos_text, True, white)
            vel_text_render = font.render(player_vel_text, True, white)
            surf.blit(mouse_text_render, (400, 10))
            surf.blit(vel_text_render, (20, 90))
            surf.blit(cam_pos_render, (20, 50))
            pygame.draw.rect(surf, (255, 255, 0), pygame.Rect(x - self.camera_pos[0], y - self.camera_pos[1], 16, 16), True)
            pygame.draw.circle(surf, (0, 255, 0), [x - self.camera_pos[0], y - self.camera_pos[1]], 4)

        self.ansgar.draw(surf, self.camera_pos, dt)

        pygame.display.flip()
