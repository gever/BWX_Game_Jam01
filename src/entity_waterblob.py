import pygame
import pymunk 
import random

from entity_particle_water import WaterParticle
from entity_base import BaseEntity

def load():
    global assets
    assets = WaterBlobAssets()

class WaterBlobAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Water Blob.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 12))
        self.spritelist = []
        for i in range (0,3):
            frame = spritesheet.subsurface(((20*i), 0, 16, 12))
            self.spritelist.append(frame)
        self.anchor = (8, 14)

class WaterBlob(BaseEntity):
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
        tile_props = self.get_current_tile_props()
        if random.random() < 0.04:
                    particle = WaterParticle(self.level, self.body.position, (random.uniform(-50, 50), random.uniform(-100, 0)))
                    self.level.entities.append(particle)

        if tile_props and tile_props.get('water'):
            MAX_SPEED = 100
            MOVEMENT_STRENGTH = 40
        else:
            MAX_SPEED = 60
            MOVEMENT_STRENGTH = 45

        self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)

        self.die_if_tile_kills_you()
