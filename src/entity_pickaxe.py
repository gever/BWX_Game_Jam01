import pygame
import pymunk

from entity_base import BaseEntity
from player_state import player_state

def load():
    global assets
    assets = PickaxeAssets()

class PickaxeAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Pickaxe.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 16))
        self.anchor = (8, 8)

class Pickaxe(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=4, static=True)
        self.carrier = None

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    # update pick position to match player
    def act(self, dt):
        if self.carrier:
            self.body.position = (self.carrier.body.position.x+8, self.carrier.body.position.y-12)

    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            # self.remove()
            self.carrier = other_entity
            player_state.add_to_inventory('pickaxe', self)
