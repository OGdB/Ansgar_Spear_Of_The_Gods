import sys

import pygame


pygame.font.init()
import application

class Retry_screen():
    def __init__(self,screen_w,screen_h):
        self.App = application.Application(screen_w, screen_h, int(1920/4), int(1080/4))
        self.win_w = 1920/4  # window width in pixels
        self.win_h = 1080/4  # window height in pixels
        self.half_w = self.win_w /2  # half-window width in pixels
        self.half_h = self.win_h / 2  # half-window height in pixels
        self.start = pygame.display.set_mode((int(1920/4), int(1080/4)), pygame.FULLSCREEN)  # The main window
        self.done = False  # Should we bail out of the game loop?
        self.cont = False

        self.font = pygame.font.SysFont("Courier New",25)
        self.cont_surf = self.font.render("Retry?", False, (250, 255, 255))
        self.cw = self.cont_surf.get_width()
        self.fon2 = pygame.font.SysFont("Courier New", 35)
        self.yes_surf =self.fon2.render("Yes",False,(255,255,255))
        self.no_surf = self.fon2.render("No", False, (255, 255, 255))




    def run(self):
        while not self.done:
            self.handle_input()
            self.render(self.start)

        # Shut down pygame after we're done with our game loop (because the program is likely to shut down shortly after)


    def handle_input(self):
        # Process the event (make sure this is only once in your game loop!)
        evt = pygame.event.poll()

        # event-handling
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        all_keys = pygame.key.get_pressed()

        if self.half_w/2 <= mouse_x <= self.half_w/2 + 70 and self.half_h + self.half_h/2 <= mouse_y <= self.half_h + self.half_h/2 + 35:
            if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:

                self.App.done = False
                self.App.clock.tick()
                self.App.run()
                self.cont = True
                self.done = True
        if  self.half_w + self.half_w/2 <= mouse_x <= self.half_w + self.half_w/2 + 70 and self.half_h + self.half_h/2 <= mouse_y <= self.half_h + self.half_h/2 + 35:
            if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                pygame.quit()
                sys.exit()



    def render(self, surf):
        # Clean up whatever is drawn and redraw
        surf.fill((0, 0, 0))
        surf.blit(self.cont_surf,(self.half_w,150))
        surf.blit(self.yes_surf,(self.half_w/2,self.half_h+self.half_h/2))
        surf.blit(self.no_surf,(self.half_w+self.half_w/2,self.half_h+self.half_h/2))

        pygame.display.flip()