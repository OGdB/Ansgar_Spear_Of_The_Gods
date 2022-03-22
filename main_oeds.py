import pygame
import Classes.platform as plf

pygame.init()

win = pygame.display.set_mode((960, 640))
clock = pygame.time.Clock()

t_f = plf.Platform(50, 50, 20, 20)

mouse_spr = plf.Platform(100, 100, 20, 20)

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
platforms.add(t_f)  # add test sprite to group

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

    mouse_pos = pygame.mouse.get_pos()
    mouse_spr.move(mouse_pos[0] - mouse_spr.image.get_width() / 2, mouse_pos[1] - mouse_spr.image.get_height() / 2)

    if pygame.Rect.colliderect(mouse_spr.rect, t_f.rect):
        print("collision")

    # DRAWING
    win.fill((0, 0, 0))

    t_f.draw(win)
    mouse_spr.draw(win)

    pygame.display.flip()

pygame.quit()
