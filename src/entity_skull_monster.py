import pygame
import pymunk

from collision_types import *
from entity_base import BaseEntity

def load():
    global assets
    assets = SkullMonsterAssets()

class SkullMonsterAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/2D Dungeon Asset Pack_v5.2/character and tileset/Dungeon_Enemy_v2.png').convert_alpha()
        self.sprite = spritesheet.subsurface((32, 0, 16, 16))
        self.anchor = (8, 14)

class SkullMonster(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)

        self.sprite = assets.sprite
        self.anchor = assets.anchor

        self.body = pymunk.Body(1, float('inf'))
        self.body.position = self.initial_pos
        self.shape = pymunk.Circle(self.body, 6)
        self.shape.collision_type = COLLISION_TYPE_OTHER_ENTITY
        self.shape.elasticity = 0
        self.level.space.add(self.body, self.shape)

    def get_render_info(self):
        return {
            'sprite': self.sprite,
            'pos': self.body.position,
            'anchor': self.anchor,
        }

    def act(self):
        MAX_SPEED = 85
        MOVEMENT_STRENGTH = 15
        self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)
