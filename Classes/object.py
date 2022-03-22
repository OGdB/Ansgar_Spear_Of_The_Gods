class Object:
    """Base class for an object"""

    def __init__(self, start_x, start_y, static):
        self.x = start_x  # x-Position of object
        self.y = start_y  # y-Position of object

    def draw(self):
        pass