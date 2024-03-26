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
        #keys = pygame.key.get_pressed()
        #if self.check_1 or self.check_2 or self.check_3 or self.check_4 or self.check_5 or self.check_6 or self.check_7 or self.check_8 or self.check_9 or self.check_10:
        #    any_check = True
        #if self.check_10 == True and keys[pygame.K_RETURN] or keys[pygame.K_SPACE] and self.check_10 == True:
        #    self.konami = True
        #    print("bomb deployed")
        #elif self.check_9 == True:
        #    if keys[pygame.K_z]:
        #       self.check_10 = True
        #       self.check_9 = False
        #       print("self.check_9 done")
        #    elif not keys[pygame.K_x]:
        #        self.check_9 = False
        #elif self.check_8 == True:
        #    if keys[pygame.K_x]:
        #        self.check_9 = True
        #        self.check_8 = False
        #        print("self.check_9 done")
        #   elif not keys[pygame.K_x]:
        #        self.check_8 = False
        #elif self.check_7 == True:
        #    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        #        self.check_8 = True
        #        self.check_7 = False
        #        print("self.check_8 done")
        #    elif not keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        #        self.check_7 = False
        #elif self.check_6 == True:
        #    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #        self.check_7 = True
        #        self.check_6 = False
        #        print("self.check_7 done")
        #    elif not keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #        self.check_6 = False
        #elif self.check_5 == True:
        #    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        #        self.check_6 = True
        #        self.check_5 = False
        #        print("self.check_6 done")
        #    elif not keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        #        self.check_5 = False
        #elif self.check_4 == True:
        #    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #        self.check_5 = True
        #        self.check_4 = False
        #        print("self.check_5 done")
        #    elif not keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #        self.check_4 = False
        #elif self.check_3 == True:
        #    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #        self.check_4 = True
        #        self.check_3 = False
        #        print("self.check_4 done")
        #    elif not keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #        self.check_3 = False
        #elif self.check_2 == True:
        #    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #        self.check_3 = True
        #        self.check_2 = False
        #        print("self.check_3 done")
        #    elif not keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #        self.check_2 = False
        #elif self.check_1 == True:
        #    if keys[pygame.K_UP] or keys[pygame.K_w]:
        #        self.check_2 = True
        #        self.check_1 = False
        #        print("self.check_2 done")
        #    elif not keys[pygame.K_UP] or keys[pygame.K_w]:
        #        self.check_1 = False
        #elif not self.any_check and keys[pygame.K_UP] or keys[pygame.K_w]:
        #    self.check_1 = True
        #    print("self.check_1 done")

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
