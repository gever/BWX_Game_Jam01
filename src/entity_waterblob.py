import pygame
import pymunk

from entity_base import BaseEntity

def load():
    global assets
    assets = WaterBlobAssets()

class WaterBlobAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Water Blob.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 12))
        self.anchor = (8, 14)

class WaterBlob(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def act(self, dt):
        tile_props = self.get_current_tile_props()
        if tile_props and tile_props.get('water'):
            MAX_SPEED = 100
            MOVEMENT_STRENGTH = 40
        else:
            MAX_SPEED = 40
            MOVEMENT_STRENGTH = 25

        self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)

        self.die_if_tile_kills_you()
