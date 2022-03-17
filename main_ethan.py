import pygame
import enemy

pygame.init()

win = pygame.display.set_mode((960, 640))
clock = pygame.time.Clock()
enemy_group_one = enemy.Enemy(300, 300, 5)
enemy_group_two = enemy.Enemy(500, 500, 10)
enemy_group_one.create_enemy()
enemy_group_two.create_enemy()
done = False
while not done:
    delta_time = clock.tick() / 1000

    # UPDATE
    enemy_group_one.update(delta_time)
    enemy_group_two.update(delta_time)

    # INPUT
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        done = True
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_ESCAPE]:
        done = True

    # DRAWING
    win.fill((0, 0, 0))
    enemy_group_one.draw(win)
    enemy_group_two.draw(win)

    pygame.display.flip()

pygame.quit()
