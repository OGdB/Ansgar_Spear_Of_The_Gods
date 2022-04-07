import pygame
import application
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
        self.playing = False
        self.font = pygame.font.SysFont("Courier New", 30)  # The font to use for rendering stats
        self.play_surf = self.font.render("Play", False, (0, 255, 255))
        self.credits_surf = self.font.render("Credits", False,(0,255,255))
        self.pw = self.play_surf.get_width()
        self.cw = self.credits_surf.get_width()
        self.start_img = pygame.image.load("image\\start_screenfn.png")
        self.scaled_img = pygame.transform.scale(self.start_img, (screen_w, screen_h))
        self.App = application.Application(screen_w, screen_h)
        self.credits = False
        self.crdfont = pygame.font.SysFont("Courier New", 50)  # The font to use for rendering stats
        self.credits1 = self.crdfont.render("Oeds deBoer", False, (0, 255, 255))
        self.credits2 = self.crdfont.render("Stan Van den Akker", False, (0, 255, 255))
        self.credits3 = self.crdfont.render("Ethan Knowles", False, (0, 255, 255))
        self.credits4 = self.crdfont.render("Tyler Howard", False, (0, 255, 255))

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
        count = 0
        if self.half_h+150 <= mouse_y <= self.half_h+185 and self.half_w-50 <= mouse_x <= self.half_w-50+self.pw+5:
            if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                self.done = True
                self.playing = True

        if self.half_h + 150 <= mouse_y <= self.half_h + 185 and self.half_w - 410 <= mouse_x <= self.half_w - 410 + self.cw + 5:
            if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                if self.credits == False:
                    self.credits = True
                else:
                    self.credits = False

    def render(self, surf):
        # Clean up whatever is drawn and redraw
        surf.fill((0, 0, 0))
        surf.blit(self.scaled_img,(-175,0))
        pygame.draw.rect(surf,(0,0,0),(self.half_w-50,self.half_h+150,self.pw+5,35))
        pygame.draw.rect(surf, (0, 0, 0), (self.half_w - 410, self.half_h + 150, self.cw + 5, 35))
        surf.blit(self.play_surf,(self.half_w-50,self.half_h+150))
        surf.blit(self.credits_surf,(self.half_w-410,self.half_h+150))
        if self.credits == True:
            surf.blit(self.credits1,(150, self.half_h - 300))
            surf.blit(self.credits2,(950, self.half_h - 300))
            surf.blit(self.credits3,(150, self.half_h - 200))
            surf.blit(self.credits4,(950, self.half_h - 200))
        pygame.display.flip()