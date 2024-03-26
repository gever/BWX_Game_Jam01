import pygame
from pygame.locals import *

class PlayerState:
    def __init__(self):
        self.reset()
        self.total_lives = 5
        self.konami = False
        self.set_values = True
    def reset(self):
        self.health = 5
        self.inventory = {}
    def restart(self):
        self.health = 5
        self.inventory = {}
        self.total_lives = 5
    def apply_damage(self):
        self.health -= 1
        print(self.health)
    def konami_check(self):
        if self.set_values:
            self.check_1 = False
            self.check_2 = False
            self.check_3 = False
            self.check_4 = False
            self.check_5 = False
            self.check_6 = False
            self.check_7 = False
            self.check_8 = False
            self.check_9 = False
            self.check_10 = False
            self.any_check = False
            self.set_values = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN and self.check_10 == True:
                    self.konami = True
                    print("check 11 done, konami initiated")
                elif event.key == K_z and self.check_9 == True:
                    self.check_10 = True
                    print("check 10 done")
                elif event.key == K_x and self.check_8 == True:
                    self.check_9 = True
                    print("check 9 done")
                elif event.key == K_d and self.check_7 == True:
                    self.check_8 = True
                    print("check 8 done")
                elif event.key == K_a and self.check_6 == True:
                    self.check_7 = True
                    print("check 7 done")
                elif event.key == K_d and self.check_5 == True:
                    self.check_6 = True
                    print("check 6 done")
                elif event.key == K_a and self.check_4 == True:
                    self.check_5 = True
                    print("check 5 done")
                elif event.key == K_s and self.check_3 == True:
                    self.check_4 = True
                    print("check 4 done")
                elif event.key == K_s and self.check_2 == True:
                    self.check_3 = True
                    print("check 3 done")
                elif event.key == K_w and self.check_1 == True:
                    self.check_2 = True
                    print("check 2 done")
                elif event.key == K_w and self.any_check == False:
                    self.check_1 = True
                    print("check 1 done")

    def add_to_inventory(self, label, item):
        self.inventory[label] = item

    def inventory_contains(self, label):
        return label in self.inventory

    def remove_from_inventory(self, label):
        # self.inventory.remove(label)
        del self.inventory[label]
    def get_item(self, label):
        if label in self.inventory:
            return self.inventory[label]
        else:
            return None


player_state = PlayerState()
