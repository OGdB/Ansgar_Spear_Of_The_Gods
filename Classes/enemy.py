import pygame.image
import Classes.enemy_spawner
import Classes.health


def draw_all_arrows(arrow_list, surf, cam_pos):
    for cur_box in arrow_list:
        x = cur_box[0] - cam_pos[0]
        y = (cur_box[1] - 10) - cam_pos[1]
        size = cur_box[2]
        color = cur_box[3]
        surf.blit(pygame.image.load("image\\Fireball.png"), (x, y))


class EnemyGroups:

    def __init__(self, x, y, num, size, r_b, enemy_type, cam_pos):
        """ Creates the group of enemy's based on the information provided. THe starting x and y, how many in this
            group, then how much the enemy's have. """
        self.position = [x, y]
        self.cam_pos = cam_pos
        self.enemy_list = []
        self.arrow_list = []
        self.num = num
        self.type = enemy_type
        self.r_border = r_b
        if self.type == 1:
            self.size = size
        elif self.type == 2:
            self.size = size
        elif self.type == 3:
            self.size = size

        i = 0
        while i < self.num:
            new_x = self.position[0]
            new_y = self.position[1]
            new_enemy = Classes.enemy_spawner.Enemy_Spawner(new_x, new_y, self.size, self.type)
            self.enemy_list.append(new_enemy)
            i += 1

    def update(self, dt, hero_x, hero_y):
        """ Move's the enemy's within the provided limits. Calls the update in the enemy_spawner class. """
        j = 0
        while j < len(self.enemy_list):

            self.enemy_list[j].update(dt, self.position[0], self.r_border,
                                      hero_x, hero_y, self.arrow_list, False)
            if self.enemy_list[j].dead:
                self.enemy_list.remove(self.enemy_list[j])
            j += 1
        for a in self.arrow_list:
            a[0] += a[4] * dt

    def enemy_hit_check(self, spear_x, spear_y_top, spear_y_bot, dmg):
        """ Checks to see if the enemy has been hit. """
        i = 0
        while i < len(self.enemy_list):
            hit, tank = self.enemy_list[i].enemy_hit_check(spear_x, spear_y_top, spear_y_bot)
            if hit:
                if tank > 0:
                    dead = self.enemy_list[i].health.take_damage(dmg - tank)
                else:
                    dead = self.enemy_list[i].health.take_damage(dmg)
                if dead:
                    self.enemy_list[i].dead = True
                    return True
            i += 1

    def enemy_attack_check(self, hero_rect):
        i = 0
        dmg = 0
        force = 0
        direction = 0
        while i < len(self.enemy_list):
            dmg, force, direction = self.enemy_list[i].enemy_attack_check(hero_rect, self.arrow_list)
            i += 1
        return dmg, force, direction

    def draw(self, win, dt):
        """ Draw's the enemy's. Calls the draw in the enemy_spawner class. """
        for cur_enemy in self.enemy_list:
            cur_enemy.draw(win, dt, self.cam_pos)
        draw_all_arrows(self.arrow_list, win, self.cam_pos)
