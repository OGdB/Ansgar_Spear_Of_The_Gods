import enemy_spawner


class Enemy:
    def __init__(self, x, y, num):
        self.position = [x, y]
        self.enemy_list = []
        self.num = num
        enemy_spawner.Enemy_Spawner.dim = 16

    def create_enemy(self):
        i = 0
        while i <= self.num:
            new_x = self.position[0]
            new_y = self.position[1]
            new_enemy = enemy_spawner.Enemy_Spawner(new_x, new_y)
            self.enemy_list.append(new_enemy)
            i += 1

    def update(self, dt):
        j = 0
        while j < len(self.enemy_list):
            self.enemy_list[j].update(dt, 800, 600)
            if self.enemy_list[j].health <= 0:
                self.enemy_list.remove(self.enemy_list[j])
            j += 1

    def draw(self, win):
        for cur_enemy in self.enemy_list:
            cur_enemy.draw(win)
