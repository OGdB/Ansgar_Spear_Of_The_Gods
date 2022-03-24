import pygame
import Classes.enemy

pygame.init()

win = pygame.display.set_mode((960, 640))
clock = pygame.time.Clock()
enemy_group_one = Classes.enemy.EnemyGroups(300, 300, 5, 16)  # The starting x and y value of the enemy, then how many, then the health
enemy_group_two = Classes.enemy.EnemyGroups(800, 500, 10, 16)
done = False
while not done:
    delta_time = clock.tick() / 1000

    # UPDATE
    enemy_group_one.update(delta_time, 300, 900)  # Moves the enemy's with in the given range
    enemy_group_two.update(delta_time, 100, 600)

    # INPUT
    event = pygame.event.poll()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        enemy_group_one.enemy_hit_check(mouse_x, mouse_y, 100)
        enemy_group_two.enemy_hit_check(mouse_x, mouse_y, 100)
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
