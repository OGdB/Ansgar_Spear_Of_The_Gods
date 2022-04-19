import pygame
import Classes.hero
import pymunk
pygame.init()

class Start_screen():
    def __init__(self,screen_w,screen_h):
        self.win_w = screen_w  # window width in pixels
        self.win_h = screen_h  # window height in pixels
        self.half_w = self.win_w /2  # half-window width in pixels
        self.half_h = self.win_h / 2  # half-window height in pixels
        self.start = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # The main window
        self.done = False  # Should we bail out of the game loop?
        self.cont = False
        self.font = pygame.font.SysFont("Courier New", 30)  # The font to use for rendering stats
        self.cont_surf = self.font.render("Continue?", False, (0, 255, 255))
        self.cw = self.cont_surf.get_width()
        self.death_img = pygame.image.load("image\\Main_Background.png")
        self.scaled_img = pygame.transform.scale(self.death_img, (screen_w, screen_h))


    def run(self):
        while not self.done:
            self.handle_input()
            self.render(self.start)

        # Shut down pygame after we're done with our game loop (because the program is likely to shut down shortly after)
        pygame.quit()

    def handle_input(self):
        # Process the event (make sure this is only once in your game loop!)
        evt = pygame.event.poll()

        # event-handling
        if evt.type == pygame.QUIT:
            self.done = True
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                self.done = True

        mouse_x, mouse_y = pygame.mouse.get_pos()
        all_keys = pygame.key.get_pressed()


    def render(self, surf):
        # Clean up whatever is drawn and redraw
        surf.fill((0, 0, 0))
        surf.blit(self.scaled_img,(0,0))
        pygame.draw.rect(surf,(0,0,0),(self.half_w-50,self.half_h+150,self.cw+5,35))
        pygame.draw.rect(surf, (0, 0, 0), (self.half_w - 410, self.half_h + 150, self.cw + 5, 35))
        surf.blit(self.cont_surf,(self.half_w-50,self.half_h+150))

        pygame.display.flip()