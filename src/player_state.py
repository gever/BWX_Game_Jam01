class PlayerState:
    def __init__(self):
        self.reset()
        self.total_lives = 5
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

    def konami_check(self, event, key):
        while event in pygame.event.get(): 
            if event.type == pygame.KEYUP or event.type == pygame.K_w:
                print("You pressed the right key!")
                if event.type == pygame.KEYDOWN or event.type == pygame.K_s:
                    print("You pressed the right key!")
                    if event.type == pygame.KEYDOWN or event.type == pygame.K_s:
                        print("You pressed the right key!")
                        if event.type == pygame.KEYLEFT or event.type == pygame.K_a:
                            print("You pressed the right key!")
                            if event.type == pygame.KEYRIGHT or event.type == pygame.K_d:
                                print("You pressed the right key!")
                                if event.type == pygame.KEYLEFT or event.type == pygame.K_a:
                                    print("You pressed the right key!")
                                    if event.type == pygame.KEYRIGHT or event.type == pygame.K_d:
                                        print("You pressed the right key!")
                                        if event.type == pygame.K_x:
                                            print("You pressed the right key!")
                                            if event.type == pygame.K_z:
                                                print("You pressed the right key!")
                                                if event.type == pygame.K_RETURN:
                                                    print("You pressed the right key!")
                                                    self.konami = True
    
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