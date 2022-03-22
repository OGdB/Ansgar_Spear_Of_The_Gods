import Classes.collisionobject as collision

class RigidObject(collision.CollisionObject):
    def __init__(self, x, y, w, h):
        collision.CollisionObject.__init__(self, x, y, w, h)
        self.vel = [0, 0]
        self.grounded = False

    # TODO: Should probably call this gravity_update in Player class
    # When not on the ground, constantly decrease vel.y as long as not grounded.
    def gravity(self, dt):
        if not self.grounded:  # could add a max falling speed here too
            self.vel[1] += dt
        if self.vel[1] > 0 and self.grounded:  # if falling downwards but on the ground, set vel.y to 0.
            self.vel[1] = 0

    def push(self, force):
        self.vel[0] += force[0]
        self.vel[1] += force[1]

    def vel_move(self, pos):
        """Movement by the rigidbody, taking into account collision"""
        # changing position with velocity
        pos[1] += self.vel[1]
        return pos
