import pygame
import pymunk

from entity_base import BaseEntity

def load():
    global assets
    assets = RockAssets()

class RockAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/objects.png').convert_alpha()
        self.sprite = spritesheet.subsurface((1, 1, 35, 25))
        self.anchor = (17, 15)

class Rock(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=12, static=True)

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
