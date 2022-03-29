import pygame
import map_data
import Classes.enemy
import Classes.hero


class Application:
    def __init__(self, screen_w, screen_h):
        pygame.init()
        self.win_w = screen_w                                           # window width in pixels
        self.win_h = screen_h                                           # window height in pixels
        self.half_w = self.win_w // 2                                   # half-window width in pixels
        self.half_h = self.win_h // 2                                   # half-window height in pixels
        self.win = pygame.display.set_mode((self.win_w, self.win_h))    # The main window
        self.done = False                                               # Should we bail out of the game loop?
        self.clock = pygame.time.Clock()                                # The pygame clock object used for delta-time

        self.font = pygame.font.SysFont("Courier New", 16)              # The font to use for rendering stats

        self.cur_map = map_data.Map("maps\\Map.json")               # The initial map to load
        self.total_time = 0                   # Total time the game's been running (used for player/coin color
                                              # modulation)
        self.enemy_group_one = Classes.enemy.EnemyGroups(0, 150, 5, 16, "image\\Skeleton head.png")
        self.enemy_group_two = Classes.enemy.EnemyGroups(0, 300, 10, 16, "image\\Skeleton head.png")
        self.a = Classes.hero.Ansgar(240, 220, self.enemy_group_one, self.enemy_group_two)

    def run(self):
        while not self.done:
            delta_time = self.clock.tick() / 1000
            self.handle_input(delta_time)
            self.render(self.win)

        # Shut down pygame after we're done with our game loop (because the program is likely to shut down shortly
        # after)
        pygame.quit()

    def handle_input(self, dt):
        # Process the event (make sure this is only once in your game loop!)
        evt = pygame.event.poll()
        self.enemy_group_one.update(dt, 0, self.win_w)  # Moves the enemy's with in the given range
        self.enemy_group_two.update(dt, 0, self.win_w)
        # event-handling

        all_keys = pygame.key.get_pressed()
        if evt.type == pygame.QUIT:
            self.done = True
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                self.done = True
        self.a.update(dt, evt, all_keys)

    def render(self, surf):
        # Erase
        surf.fill((0, 0, 0))

        # Draw the map
        surf.blit(self.cur_map.rendered_img, (0, 0), (0, 0, self.win_w, self.win_h))
        self.a.draw(surf)
        self.enemy_group_one.draw(surf)
        self.enemy_group_two.draw(surf)

        # Flip
        pygame.display.flip()

