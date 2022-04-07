import pygame.image
import Classes.enemy_spawner
import Classes.health


class EnemyGroups:

    def __init__(self, x, y, num, size, l_b, enemy_type):
        """ Creates the group of enemy's based on the information provided. THe starting x and y, how many in this
            group, then how much the enemy's have. """
        self.position = [x, y]
        self.enemy_list = []
        self.arrow_list = []
        self.num = num
        Classes.enemy_spawner.Enemy_Spawner.dim = size
        self.type = enemy_type
        self.l_border = l_b
        if self.type == 1:
            self.image = pygame.image.load("image\\Bear.png")
        elif self.type == 2:
            self.image = pygame.image.load("image\\Fire_Bear.png")
        i = 0
        while i < self.num:
            new_x = self.position[0]
            new_y = self.position[1]
            new_enemy = Classes.enemy_spawner.Enemy_Spawner(new_x, new_y, self.type)
            self.enemy_list.append(new_enemy)
            i += 1

    def update(self, dt, hero_x, hero_y):
        """ Move's the enemy's within the provided limits. Calls the update in the enemy_spawner class. """
        j = 0
        while j < len(self.enemy_list):

            self.enemy_list[j].update(dt, self.position[0], self.l_border, hero_x, hero_y, self.arrow_list, False)
            if self.enemy_list[j].dead:
                self.enemy_list.remove(self.enemy_list[j])
            j += 1

    def enemy_hit_check(self, spear_x, spear_y_top, spear_y_bot, dmg):
        """ Checks to see if the enemy has been hit. """
        i = 0
        while i < len(self.enemy_list):
            hit = self.enemy_list[i].enemy_hit_check(spear_x, spear_y_top, spear_y_bot)
            if hit:
                dead = self.enemy_list[i].health.take_damage(dmg)
                if dead:
                    self.enemy_list[i].dead = True
                    return True
            i += 1

    def enemy_attack_check(self, hero_rect):
        i = 0
        dmg = 0
        while i < len(self.enemy_list):
            dmg += self.enemy_list[i].enemy_attack_check(hero_rect, self.arrow_list)
            i += 1
        return dmg

    def draw(self, win):
        """ Draw's the enemy's. Calls the draw in the enemy_spawner class. """
        for cur_enemy in self.enemy_list:
            cur_enemy.draw(win, self.arrow_list, self.image)
