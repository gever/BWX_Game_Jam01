class PlayerState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.health = 5
        self.inventory = {}

    def apply_damage(self):
        self.health -= 1
        print(self.health)

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
