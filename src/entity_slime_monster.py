import pygame
import pymunk 

from entity_base import BaseEntity

def load():
    global assets
    assets = SlimeMonsterAssets()

class SlimeMonsterAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Mushroom man.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 21, 23))
        self.spritelist = []
        for i in range(0,4):
            frame = spritesheet.subsurface(((23*i), 0, 21, 23))
            self.spritelist.append(frame)
        self.anims = {
            'left': self.spritelist[0:2],
            'right': self.spritelist[2:4],
        }
        self.anchor = (8, 14)

class SlimeMonster(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)
        self.current_anim = 'right'
        self.anim_phase = 0

    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            other_entity.remove()

    def get_render_info(self):
        anim = assets.anims[self.current_anim]
        frame = int(self.anim_phase * len(anim)) % len(anim)
        return {
            'sprite': anim[frame],
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def act(self, dt):
        self.anim_phase += dt
        self.current_anim = 'left' if (self.body.velocity.x > 0) else 'right'

        MAX_SPEED = 100
        MOVEMENT_STRENGTH = 110
        self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)

        self.die_if_tile_kills_you()
