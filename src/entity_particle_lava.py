import pygame

from entity_particle import ParticleEntity

def load():
    global assets
    assets = LavaParticleAssets()

class LavaParticleAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Lava Blob.png').convert_alpha()
        self.sprite = spritesheet.subsurface((5, 5, 2, 2))
        self.anchor = (1, 1)

class LavaParticle(ParticleEntity):
    def __init__(self, level, initial_pos, initial_velo):
        super().__init__(level, initial_pos, initial_velo)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }
