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
        spritesheet = pygame.image.load('../gfx/Crate.png').convert_alpha()
        burningspritesheet = pygame.image.load('../gfx/Crate  burning.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 16))
        self.burning_sprite = burningspritesheet.subsurface((0, 0, 16, 16))
        self.anchor = (8, 8)

class Crate(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=6, square=True)
        self.in_lava_since = None  # Track when the crate entered the lava

    def get_render_info(self):
        tile_props = self.get_current_tile_props()
        in_lava = tile_props and tile_props.get('kills you')
        if in_lava and self.in_lava_since is None:
            self.in_lava_since = time.time()  # Start timing when first entering lava
        elif not in_lava:
            self.in_lava_since = None  # Reset if not in lava
        return {
            'sprite': assets.burning_sprite if in_lava else assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def act(self, dt):
        self.apply_force_to_achieve_velocity(pymunk.Vec2d(0, 0), strength=50)
        if self.in_lava_since and time.time() - self.in_lava_since > .5:
            self.remove_from_level()  # Custom method to remove the crate from the level

    def remove_from_level(self):
        # Assuming there's a method in BaseEntity or level to remove an entity
        self.remove()
    