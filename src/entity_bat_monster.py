import pygame
import pymunk

from entity_base import BaseEntity

def load():
    global assets
    assets = BatMonsterAssets()

class BatMonsterAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/bat_sprite.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 12))
        self.anchor = (8, 8)
        self.spritelist = []
        for i in range (0,2):
            frame = spritesheet.subsurface(((17*i), 0, 16, 12))
            self.spritelist.append(frame)

class BatMonster(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)
        self.timer = 0

    def get_render_info(self):
        frame = int(self.timer) % len(assets.spritelist)
        return {
            'sprite': assets.spritelist[frame],
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def act(self, dt):
        self.timer += dt*7
        MAX_SPEED = 85
        MOVEMENT_STRENGTH = 15
        self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)
