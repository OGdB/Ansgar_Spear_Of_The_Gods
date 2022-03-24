import pygame
import Classes.hero

pygame.init()

win = pygame.display.set_mode((480, 320),pygame.RESIZABLE)
clock = pygame.time.Clock()
a = Classes.hero.Ansgar(240,220)

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

    a.update(delta_time,event, all_keys)

    # DRAWING
    win.fill((0, 0, 0))
    a.draw(win)

    pygame.display.flip()

pygame.quit()
