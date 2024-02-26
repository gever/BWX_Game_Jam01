import pygame
import pymunk

from entity_base import BaseEntity

def load():
    global assets
    assets = RockAssets()

class RockAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/2D Dungeon Asset Pack_v5.2/character and tileset/Dungeon_Enemy_v2.png').convert_alpha()
        self.sprite = spritesheet.subsurface((32, 0, 16, 16))
        self.anchor = (8, 14)

class Rock(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def act(self):
        MAX_SPEED = 0
        MOVEMENT_STRENGTH = 500
        self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)
