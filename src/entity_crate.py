import pygame
import pymunk
import time

from entity_base import BaseEntity
from player_state import player_state
from audio import get_audio

def load():
    global assets
    assets = CrateAssets()

class CrateAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/2D Dungeon Asset Pack_v5.2/character and tileset/Dungeon_item_props_v2.png').convert_alpha()
        self.sprite = spritesheet.subsurface((112, 48, 16, 16))
        self.anchor = (8, 8)

class Crate(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=7, square=True)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def act(self,dt):
        self.apply_force_to_achieve_velocity(pymunk.Vec2d(0,0),strength=50)
