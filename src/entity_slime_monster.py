import pygame
import pymunk

from collision_types import *
from entity_base import BaseEntity

def load():
    global assets
    assets = SlimeMonsterAssets()

class SlimeMonsterAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/2D Dungeon Asset Pack_v5.2/character and tileset/Dungeon_Enemy_v2.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 16))
        self.anchor = (8, 14)

class SlimeMonster(BaseEntity):
    def __init__(self, space, initial_pos):
        self.sprite = assets.sprite
        self.anchor = assets.anchor
        self.space = space

        self.body = pymunk.Body(1, float('inf'))
        self.body.position = initial_pos
        self.shape = pymunk.Circle(self.body, 6)
        self.shape.collision_type = COLLISION_TYPE_OTHER_ENTITY
        self.shape.elasticity = 0
        space.add(self.body, self.shape)

    def get_render_info(self):
        return {
            'sprite': self.sprite,
            'pos': self.body.position,
            'anchor': self.anchor,
        }

    def move_towards_player(self, player):
        MAX_SPEED = 30
        MOVEMENT_STRENGTH = 120

        pos_diff = player.body.position - self.body.position
        if pos_diff.length > 0:
            desired_velocity = pos_diff.normalized() * MAX_SPEED
        else:
            desired_velocity = pymunk.Vec2d(0, 0)
        self.apply_force_to_achieve_velocity(desired_velocity, MOVEMENT_STRENGTH)
