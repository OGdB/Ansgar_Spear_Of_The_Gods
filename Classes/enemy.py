import Classes.enemy_spawner
import Classes.health


class EnemyGroups:

    def __init__(self, x, y, num, size):
        """ Creates the group of enemy's based on the information provided. THe starting x and y, how many in this
            group, then how much the enemy's have. """
        self.position = [x, y]
        self.enemy_list = []
        self.num = num
        self.health = Classes.health.Health()
        Classes.enemy_spawner.Enemy_Spawner.dim = size
        i = 0
        while i <= self.num:
            new_x = self.position[0]
            new_y = self.position[1]
            new_enemy = Classes.enemy_spawner.Enemy_Spawner(new_x, new_y, self.health)
            self.enemy_list.append(new_enemy)
            i += 1

    def update(self, dt, r_border_x, l_border_x):
        """ Move's the enemy's within the provided limits. Calls the update in the enemy_spawner class. """
        j = 0
        while j < len(self.enemy_list):
            self.enemy_list[j].update(dt, r_border_x, l_border_x, False)
            if self.enemy_list[j].dead:
                self.enemy_list.remove(self.enemy_list[j])
            j += 1

    def enemy_hit_check(self, mouse_x, mouse_y, dmg):
        i = 0
        while i < len(self.enemy_list):
            hit = False
            hit = self.enemy_list[i].enemy_hit_check(mouse_x, mouse_y)
            if hit:
                dead = self.enemy_list[i].health.take_damage(dmg)
                if dead:
                    self.enemy_list[i].dead = True
            i += 1

    def draw(self, win):
        """ Draw's the enemy's. Calls the draw in the enemy_spawner class. """
        for cur_enemy in self.enemy_list:
            cur_enemy.draw(win)
