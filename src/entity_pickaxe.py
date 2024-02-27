import pygame
import pymunk

from entity_base import BaseEntity
from player_state import player_state

def load():
    global assets
    assets = PickaxeAssets()

class PickaxeAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/objects.png').convert_alpha()
        self.sprite = spritesheet.subsurface((47, 1, 24, 24))
        self.anchor = (11, 16)

class Pickaxe(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=12, static=True)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            self.remove()
            player_state.add_to_inventory('pickaxe')
