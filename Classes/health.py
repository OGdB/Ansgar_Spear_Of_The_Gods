class Health:
    def __init__(self):
        self.max_health = 100
        self.cur_health = self.max_health

    def take_damage(self, amount):
        """Returns true if entity died"""
        self.cur_health -= amount

        if self.cur_health < 0:  # cannot have lower health than 0
            self.cur_health = 0
            return True  # entity died

        return False

    def increase_max_health(self, amount, heal=True):
        self.max_health += amount

        if heal:
            self.cur_health = self.max_health
