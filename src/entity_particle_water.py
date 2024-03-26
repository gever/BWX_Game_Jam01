import pygame

from entity_particle import ParticleEntity

def load():
    global assets
    assets = WaterParticleAssets()

class WaterParticleAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Splosh Effect.png').convert_alpha()
        self.sprite = spritesheet.subsurface((1, 2, 5, 5))
        self.anchor = (1, 1)

class WaterParticle(ParticleEntity):
    def __init__(self, level, initial_pos, initial_velo):
        super().__init__(level, initial_pos, initial_velo)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }