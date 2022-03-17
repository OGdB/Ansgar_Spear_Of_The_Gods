import pygame
import Classes.platform as plf

pygame.init()

win = pygame.display.set_mode((960, 640))
clock = pygame.time.Clock()

t_f = plf.Platform(50, 50, 20, 20)

done = False
while not done:
    delta_time = clock.tick() / 1000

    # INPUT
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        done = True
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_ESCAPE]:
        done = True

    # DRAWING
    win.fill((0, 0, 0))

    t_f.draw(win)

    pygame.display.flip()

pygame.quit()
