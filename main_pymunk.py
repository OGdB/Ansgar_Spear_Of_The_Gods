import pymunk
import pygame

pygame.init()
win_w = 800
win_h = 600
win = pygame.display.set_mode((win_w, win_h))
done = False
clock = pygame.time.Clock()

space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = (0, 200)  # Set its gravity

ground_points = ((0, 550), (50, 600), (750, 500))

for i in range(len(ground_points) - 1):  # For loop creating and setting the attributes of the ground points.
    seg = pymunk.Segment(space.static_body, ground_points[i], ground_points[i + 1], 0.0)
    seg.elasticity = 0.95
    seg.friction = 0.9
    space.add(seg)

ball_list = []

while not done:  # Infinite loop simulation
    delta_time = clock.tick(60) / 1000
    space.step(delta_time)  # Step the simulation one step forward

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        body = pymunk.Body()  # Create a Body
        body.position = event.pos  # Set the position of the body
        body_radius = 30
        body_shape = pymunk.Circle(body, body_radius)
        body_shape.mass = 10
        space.add(body, body_shape)
        ball_list.append(body)

    win.fill((0, 0, 0))

    for body in ball_list:
        pygame.draw.circle(win, (255, 0, 0), body.position, body_radius)
    for i in range(len(ground_points) - 1):
        pygame.draw.line(win, (100, 100, 255), ground_points[i], ground_points[i + 1])
    pygame.display.flip()

pygame.quit()
