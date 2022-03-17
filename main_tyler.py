import pygame


class Ansgar():
    def __init__(self,player_x,player_y):
        self.position = [player_x,player_y]

    def draw(self, surf):
        pygame.draw.rect(surf,(255,255,0),(self.position[0],self.position[1],64,64))

    def update(self,dt):
        all_keys = pygame.key.get_pressed()
        if all_keys[pygame.K_a] or all_keys[pygame.K_LEFT]:
            if all_keys[pygame.K_LSHIFT]:
                self.position[0] -= 150 * dt
            else:
                self.position[0] -= 75 * dt
        if all_keys[pygame.K_d] or all_keys[pygame.K_RIGHT]:
            if all_keys[pygame.K_LSHIFT]:
                self.position[0] += 150 * dt
            else:
                self.position[0] += 75 * dt

pygame.init()

win = pygame.display.set_mode((960, 640),pygame.RESIZABLE)
clock = pygame.time.Clock()
a = Ansgar(200,200)

done = False
while not done:
    #Update
    delta_time = clock.tick() / 1000


    # INPUT
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        done = True
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_ESCAPE]:
        done = True

    a.update(delta_time)

    # DRAWING
    win.fill((0, 0, 0))
    a.draw(win)
    pygame.display.flip()

pygame.quit()
