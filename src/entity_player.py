import pygame
import pymunk

from config import *
from collision_types import *
from entity_base import BaseEntity
from vec2 import Vec2

def load():
    global assets
    assets = PlayerAssets()

class PlayerAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Sprout Lands - Sprites - premium pack/Characters/Basic Charakter Spritesheet.png').convert_alpha()
        self.sprites = []
        for i in range(0, 4):
            frame = spritesheet.subsurface((16*(3*i + 1), 16, 16, 16))
            self.sprites.append(frame)
        self.anchor = (7, 12)

# It is convenient to create an instance of the player in each level, rather than "moving" the player between levels
class Player(BaseEntity):
    def __init__(self, space, initial_pos):
        self.anchor = assets.anchor
        self.sprites = assets.sprites
        self.framenum = 0
        self.space = space

        self.body = pymunk.Body(1, float('inf'))
        self.body.position = initial_pos
        self.shape = pymunk.Circle(self.body, 6)
        self.shape.collision_type = COLLISION_TYPE_PLAYER
        self.shape.elasticity = 0
        space.add(self.body, self.shape)

    def get_render_info(self):
        return {
            'sprite': self.sprites[self.framenum],
            'pos': self.body.position,
            'anchor': self.anchor,
        }

    def handle_input(self, keys, events, dt):
        # determine desired player velocity based on keyboard input
        desired_velo = Vec2()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            desired_velo += Vec2(-1, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            desired_velo += Vec2(1, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            desired_velo += Vec2(0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            desired_velo += Vec2(0, 1)

        # normalize and scale desired velocity
        if not desired_velo.is_zero():
            desired_velo = desired_velo.normalized() * PLAYER_SPEED

        # apply force to player body to make its velocity approach the desired velocity
        self.apply_force_to_achieve_velocity(desired_velo, PLAYER_MOVEMENT_MAX_ACCEL)

        # # update player sprite frame
        # if desired_velo.is_zero():
        #     self.player.anim_standing()
        # else:
        #     self.player.anim_walking(dt)
