class PlayerState:
    def __init__(self):
        self.health = 5
    
    def apply_damage(self):
        self.health -= 1
        print(self.health)

player_state = PlayerState()
