import pygame
import pymunk

from entity_base import BaseEntity

def load():
    global assets
    assets = BatMonsterAssets()

class BatMonsterAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/bat_sprite.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 9))
        self.anchor = (8, 8)

class BatMonster(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def act(self, dt):
        MAX_SPEED = 85
        MOVEMENT_STRENGTH = 15
        self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)
