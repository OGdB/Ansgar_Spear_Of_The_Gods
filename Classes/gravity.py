class Gravity:
    def __init__(self, gravity_strength=1):
        self.grav_str = gravity_strength

    def do_gravity_stuff(self, y):
        y -= self.grav_str
