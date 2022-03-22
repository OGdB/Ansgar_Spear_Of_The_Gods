import pygame
import enemy

pygame.init()

win = pygame.display.set_mode((960, 640))
clock = pygame.time.Clock()
enemy_group_one = enemy.Enemy(300, 300, 5, 100)  # The starting x and y value of the enemy, then how many, then the health
enemy_group_two = enemy.Enemy(800, 500, 10, 100)
done = False
while not done:
    delta_time = clock.tick() / 1000

    # UPDATE
    enemy_group_one.update(delta_time, 300, 900)  # Moves the enemy's with in the given range
    enemy_group_two.update(delta_time, 100, 600)

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
