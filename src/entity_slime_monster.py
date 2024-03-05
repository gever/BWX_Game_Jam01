import pygame
import pymunk

from entity_base import BaseEntity

def load():
    global assets
    assets = SlimeMonsterAssets()

class SlimeMonsterAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Mushroom Monster.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 30, 27))
        self.anchor = (8, 14)

class SlimeMonster(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)

    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            other_entity.remove()

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def act(self, dt):
        MAX_SPEED = 100
        MOVEMENT_STRENGTH = 110
        self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)

        self.die_if_tile_kills_you()
