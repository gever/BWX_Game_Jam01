import pygame
import pymunk

from entity_base import BaseEntity
from player_state import player_state
from audio import get_audio

def load():
    global assets
    assets = RockAssets()

class RockAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/The Rock.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 33, 27))
        self.anchor = (17, 15)

class Rock(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=18, static=True)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            if player_state.inventory_contains('pickaxe'):
                self.remove()
                player_state.remove_from_inventory('pickaxe')
                get_audio().play_sfx('mine_rock')
