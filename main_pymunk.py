import pymunk  # Import pymunk..
import pygame
import math
import random

# Normal pygame setup
pygame.init()
win_w = 800
win_h = 600
win = pygame.display.set_mode((win_w, win_h))
done = False
clock = pygame.time.Clock()

# The space keeps track of all physics objects, gravity, etc.
space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = (0, 0.0005)  # Set its gravity

# Define the static objects in OUR format (used for drawing)
ground_points = ((10, 550), (50, 600), (750, 500))  # a series of connected points, drawn as a line
static_boxes = [(400, 300, 50, 50), (500, 310, 50, 50)]  # a series of pygame-style rects
# ... for this one, I'm going in the reverse order.  I create a physics object, and then we
#    as IT for it's position, shape, etc. in order to draw
dynamic_physics_objects = []
dynamic_physics_objects_size = 15  # "radius" of new objects

# Create physics objects and add them to the space according to our formats from above
# ... make line segments for the ground
for i in range(len(ground_points) - 1):
    seg = pymunk.Segment(space.static_body, ground_points[i], ground_points[i + 1], 0.0)
    seg.elasticity = 0.95
    seg.friction = 0.9
    space.add(seg)
# ... make the static boxes
for b in static_boxes:
    box_pts = ((b[0], b[1]), (b[0] + b[2], b[1]), (b[0] + b[2], b[1] + b[3]), (b[0], b[1] + b[3]))
    box_shape = pymunk.Poly(space.static_body, box_pts)
    space.add(box_shape)

while not done:  # Infinite loop simulation
    delta_time = clock.tick(60)
    space.step(delta_time)  # Step the simulation one step forward

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        # Create a body and set its position to the mouse position (this is common to all shapes)
        body = pymunk.Body()  # Create a Body
        body.position = event.pos  # Set the position of the body

        # Make a sphere or block object (at random)
        body_shape = None
        if random.randint(1, 2) == 1:
            # Make a box
            angle = 0
            vertices = []
            for i in range(4):
                pt = (dynamic_physics_objects_size * math.cos(angle), dynamic_physics_objects_size * math.sin(angle))
                angle += math.pi / 2
                vertices.append(pt)
            body_shape = pymunk.Poly(body, vertices)
            body.angle = random.uniform(0, math.pi)
        else:
            body_shape = pymunk.Circle(body, dynamic_physics_objects_size)

        # Do some more setup common to all objects
        body_shape.mass = 10
        body_shape.friction = 1.05
        body_shape.elasticity = 0.1

        # Actually add the shape to our space and our list of physics objects
        space.add(body, body_shape)
        dynamic_physics_objects.append(body)

    # DRAWING
    win.fill((0, 0, 0))
    for i in range(len(dynamic_physics_objects)):
        body = dynamic_physics_objects[i]

        # body.shapes is a python set of collider shapes.  I want to get the first (and only one in our case), but
        # sets don't have that ability, so I convert it to a list and then get the first element
        shape = list(body.shapes)[0]
        if isinstance(shape, pymunk.Poly):
            angle = body.angle
            vertices = []
            for j in range(4):
                x = body.position[0] + dynamic_physics_objects_size * math.cos(-angle)
                y = body.position[1] - dynamic_physics_objects_size * math.sin(-angle)
                vertices.append((x, y))
                angle += math.pi / 2
            pygame.draw.polygon(win, (255, 0, 0), vertices)
        else:
            pygame.draw.circle(win, (255, 0, 0), body.position, dynamic_physics_objects_size)
    for i in range(len(ground_points) - 1):
        pygame.draw.line(win, (100, 100, 255), ground_points[i], ground_points[i + 1])
    for b in static_boxes:
        pygame.draw.rect(win, (100, 255, 100), b)
    pygame.display.flip()

pygame.quit()
