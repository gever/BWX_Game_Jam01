class PlayerState:
    def __init__(self):
        self.health = 5
        self.inventory = []

    def apply_damage(self):
        self.health -= 1
        print(self.health)

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def inventory_contains(self, item):
        return item in self.inventory

    def remove_from_inventory(self, item):
        self.inventory.remove(item)

player_state = PlayerState()
