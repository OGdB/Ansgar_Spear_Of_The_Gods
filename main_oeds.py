import pygame
import Classes.collisionobject as plf
import Classes.rigidobject as rigid

pygame.init()

win = pygame.display.set_mode((960, 640))
clock = pygame.time.Clock()

platforms = pygame.sprite.Group()

t_f = plf.CollisionObject(50, 50, 20, 20)
t_f2 = plf.CollisionObject(100, 50, 20, 20)
t_f3 = plf.CollisionObject(200, 300, 20, 20)
t_f4 = plf.CollisionObject(500, 500, 20, 20)
platforms.add(t_f)
platforms.add(t_f2)
platforms.add(t_f3)
platforms.add(t_f4)

mouse_spr = plf.CollisionObject(100, 100, 20, 20)

ro_pos = [400, 200]
rigid_object = rigid.RigidObject(ro_pos[0], ro_pos[1], 50, 50)

done = False
while not done:
    delta_time = clock.tick() / 1000

    # INPUT
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        done = True
    if event.type == pygame.MOUSEBUTTONUP:
        rigid_object.push((0, -1))

    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_ESCAPE]:
        done = True

    mouse_pos = pygame.mouse.get_pos()
    mouse_spr.set_pos(mouse_pos[0] - mouse_spr.image.get_width() / 2, mouse_pos[1] - mouse_spr.image.get_height() / 2)

    # if pygame.sprite.spritecollideany(mouse_spr, platforms):
    #     print("collide")

    rigid_object.gravity(delta_time)
    ro_pos = rigid_object.vel_move(ro_pos)
    rigid_object.set_pos(ro_pos[0], ro_pos[1])

    win.fill((0, 0, 0))

    mouse_spr.draw(win)
    platforms.draw(win)
    rigid_object.draw(win)

    if pygame.sprite.collide_rect(rigid_object, mouse_spr):
        rigid_object.grounded = True
        rigid_object.check_collision(mouse_spr.rect)
        mouse_spr.check_collision(rigid_object.rect)
        rigid_object.draw_collision(win)
    else:
        rigid_object.grounded = False

    pygame.display.flip()

pygame.quit()
