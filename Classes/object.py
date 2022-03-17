class Object:
    def __init__(self, start_x, start_y, static):
        self.x = start_x
        self.y = start_y
        self.static = static  # is the static or can it be moved around (and affected by gravity?)

    def draw(self):
        pass