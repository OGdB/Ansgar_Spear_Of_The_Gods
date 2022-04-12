import math

import pygame
import pymunk
import Classes.map_data
import Classes.enemy
import Classes.hero
import Classes.health

# Set to true to see a bunch of debug stuff.
debug = False


class Application:
    def __init__(self, screen_w, screen_h):
        pygame.init()
        self.win_w = screen_w  # window width in pixels
        self.win_h = screen_h  # window height in pixels
        self.half_w = self.win_w // 2  # half-window width in pixels
        self.half_h = self.win_h // 2  # half-window height in pixels
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # The main window
        self.done = False  # Should we bail out of the game loop?
        self.clock = pygame.time.Clock()  # The pygame clock object used for delta-time
        self.background = pygame.image.load("image\\Background.png")
        self.background = pygame.transform.scale(self.background, (screen_w, screen_h))
        self.space = pymunk.Space()  # Create a physics space
        self.space.gravity = (0, 250)  # Set its gravity

        self.font = pygame.font.SysFont("Courier New", 16)  # The font to use for rendering stats

        self.cur_map = Classes.map_data.Map("maps\\Map.json")  # The initial map to load
        self.total_time = 0  # Total time the game's been running (used for player/coin color modulation)
        self.ball_list = []
        self.ground_colliders = self.cur_map.draw_colliders(self.space)
        self.enemy_group_list = [
            Classes.enemy.EnemyGroups(336, (240 - 16), 3, 16, 672, 1),
            Classes.enemy.EnemyGroups(128, (480 - 16), 3, 16, 464, 1),
            Classes.enemy.EnemyGroups(848, (672 - 16), 3, 16, 1040, 1),
            Classes.enemy.EnemyGroups(0, (128 - 16), 2, 16, 80, 2),
            Classes.enemy.EnemyGroups(528, (448 - 16), 2, 16, 624, 2),
            Classes.enemy.EnemyGroups(1184, (480 - 16), 2, 16, 1456, 2),
        ]
        self.ansgar = Classes.hero.Ansgar((240, 100), self.space, self.enemy_group_list)

    def run(self):
        while not self.done:
            delta_time = self.clock.tick(60) / 1000
            self.space.step(delta_time)
            self.handle_input(delta_time)
            self.render(self.win)

        # Shut down pygame after we're done with our game loop (because the program is likely to shut down shortly after)
        pygame.quit()

    def handle_input(self, dt):
        # Process the event (make sure this is only once in your game loop!)
        evt = pygame.event.poll()
        for i in range(len(self.enemy_group_list)):
            self.enemy_group_list[i].update(dt, self.ansgar.body.position.x, self.ansgar.body.position.y)

        # event-handling
        mouse_x, mouse_y = pygame.mouse.get_pos()
        all_keys = pygame.key.get_pressed()
        if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
            body = pymunk.Body()  # Create a Body
            body.position = (mouse_x, mouse_y)  # Set the position of the body
            body_shape = pymunk.Circle(body, 10)
            body_shape.mass = 10
            self.space.add(body, body_shape)
            self.ball_list.append(body)

        if evt.type == pygame.QUIT:
            self.done = True
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                self.done = True
            if evt.key == pygame.K_F11:
                global debug
                debug = not debug
        self.ansgar.update(dt, evt, all_keys)

    def render(self, surf):
        # Drawing
        surf.fill((0, 0, 0))
        surf.blit(self.background, (0, 0))
        surf.blit(self.cur_map.rendered_img, (0, 0), (0, 0, self.win_w, self.win_h))

        for i in range(len(self.enemy_group_list)):
            self.enemy_group_list[i].draw(self.win)

        for body in self.ball_list:
            pygame.draw.circle(surf, (255, 0, 0), body.position, 10)

        # Debug drawing
        if debug:
            for platform_coordinates in self.cur_map.floor_points:
                for vertice_pairs in platform_coordinates:
                    pygame.draw.line(surf, (255, 255, 0), (vertice_pairs[0], vertice_pairs[2]),
                                     (vertice_pairs[1], vertice_pairs[2]))

            # Draw red dot on start_x of colliders
            for platform_coordinates in self.cur_map.floor_points:
                start_x = platform_coordinates[0][0]
                end_x = platform_coordinates[0][1]
                y = platform_coordinates[0][2]
                pygame.draw.circle(surf, (255, 0, 0), [start_x, y], 3)
                pygame.draw.circle(surf, (255, 255, 0), [end_x, y], 3)

            # Debug text telling you which tile-row and column is hovered over with the mouse
            # MousePos
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x = math.floor(mouse_x / self.cur_map.tile_width % self.cur_map.map_width)
            y = math.floor(mouse_y / self.cur_map.tile_height % self.cur_map.map_height)
            mouse_pos_text = f"[{x}, {y}]"

            # Velocity
            player_vel_text = f"[{math.floor(self.ansgar.body.velocity.x)}, {math.floor(self.ansgar.body.velocity.y)}]"

            white = (255, 255, 255)
            font = pygame.font.Font('freesansbold.ttf', 32)
            mouse_text_render = font.render(mouse_pos_text, True, white)
            vel_text_render = font.render(player_vel_text, True, white)
            surf.blit(mouse_text_render, (1400, 10))
            surf.blit(vel_text_render, (1400, 50))
            pygame.draw.circle(surf, (0, 255, 0), [x * 16, y * 16], 4)
            pygame.draw.rect(surf, (255, 255, 0), pygame.Rect(x * 16, y * 16, 16, 16), True)

            pygame.draw.circle(surf, (255, 0, 0), self.ansgar.body.position, 5)

        self.ansgar.draw(surf)

        pygame.display.flip()
