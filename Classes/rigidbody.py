import pygame


class Rigidbody:
    def __init__(self):
        self.vel = (0, 0)
        self.grounded = False

    # TODO: Should probably call this gravity_update in Player class
    # When not on the ground, constantly decrease vel.y as long as not grounded.
    def gravity(self, dt):
        if not self.grounded:  # could add a max falling speed here too
            vel[1] += dt * 100
        if vel[1] > 1 and self.grounded:  # if falling downwards but on the ground, set vel.y to 0.
            vel[1] = 0

    # Collision detection: https://www.pygame.org/docs/ref/rect.html#pygame.Rect.collidelist

    def move(self, pos):
        """Movement by the rigidbody, taking into account collision"""
        # changing position with velocity
        pos += vel
        return pos
