import enemy_spawner


class EnemyGroups:

    def __init__(self, x, y, num, health):
        """ Creates the group of enemy's based on the information provided. THe starting x and y, how many in this
            group, then how much the enemy's have. """
        self.position = [x, y]
        self.enemy_list = []
        self.num = num
        self.health = health
        enemy_spawner.Enemy_Spawner.dim = 16
        i = 0
        while i <= self.num:
            new_x = self.position[0]
            new_y = self.position[1]
            new_enemy = enemy_spawner.Enemy_Spawner(new_x, new_y, self.health)
            self.enemy_list.append(new_enemy)
            i += 1

    def update(self, dt, r_border_x, l_border_x):
        """ Move's the enemy's within the provided limits. Calls the update in the enemy_spawner class. """
        j = 0
        while j < len(self.enemy_list):
            self.enemy_list[j].update(dt, r_border_x, l_border_x, False)
            if self.enemy_list[j].health <= 0:
                self.enemy_list.remove(self.enemy_list[j])
            j += 1

    def draw(self, win):
        """ Draw's the enemy's. Calls the draw in the enemy_spawner class. """
        for cur_enemy in self.enemy_list:
            cur_enemy.draw(win)
