import pygame

pygame.init()

win = pygame.display.set_mode((960, 640))
clock = pygame.time.Clock()

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

    pygame.display.flip()

pygame.quit()
