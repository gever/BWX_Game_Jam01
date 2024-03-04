import pygame
import pymunk

from config import *
from entity_base import BaseEntity
from vec2 import Vec2

def load():
    global assets
    assets = PlayerAssets()

class PlayerAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/player_sprite.png').convert_alpha()
        sprites = []
        for i in range(0, 4):
            frame = spritesheet.subsurface(((17*i + 1), 1, 16, 20))
            sprites.append(frame)
        self.anims = {
            'left': list(reversed(sprites[0:2])),
            'right': sprites[2:4],
        }
        self.anchor = (7, 16)

# It is convenient to create an instance of the player in each level, rather than "moving" the player between levels:
class Player(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)

        self.current_anim = 'right'
        self.anim_phase = 0

    def get_render_info(self):
        anim = assets.anims[self.current_anim]
        frame = int(self.anim_phase * len(anim)) % len(anim)
        return {
            'sprite': anim[frame],
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def handle_input(self, keys, events, dt):
        # determine desired player velocity based on keyboard input
        desired_velo = Vec2()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            desired_velo += Vec2(-1, 0)
            self.current_anim = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            desired_velo += Vec2(1, 0)
            self.current_anim = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            desired_velo += Vec2(0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            desired_velo += Vec2(0, 1)

        # normalize and scale desired velocity
        if not desired_velo.is_zero():
            multiplier = PLAYER_SPEED
            if keys[pygame.K_SPACE]:
                multiplier += PLAYER_SPEED_BOOST
            desired_velo = desired_velo.normalized() * multiplier

        # apply force to player body to make its velocity approach the desired velocity
        self.apply_force_to_achieve_velocity(desired_velo, PLAYER_MOVEMENT_STRENGTH)

        # # update player sprite frame
        if desired_velo.is_zero():
            self.anim_phase = 0
        else:
            PLAYER_WALKING_ANIM_TIME = 0.2
            self.anim_phase += dt / PLAYER_WALKING_ANIM_TIME

    def is_player(self):
        return True

    def act(self, dt):
        self.die_if_tile_kills_you()
