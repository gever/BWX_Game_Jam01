import os

import pygame
import pymunk

from audio import get_audio
from config import *
from map import TiledMap
from vec2 import Vec2

PLAYER_ANCHOR = Vec2(7, 12)

class BaseLevel:
    def __init__(self, map_fn):
        self.map_fn = map_fn

    def start(self):
        # load Tiled map
        self.map = TiledMap(os.path.join('../maps', self.map_fn))

        # find player spawn point
        self.player_spawn_point = self.map.get_object_by_name('player_spawn')

        # create physics space
        self.space = pymunk.Space()

        # define collision type ids
        self.COLLISION_TYPE_PLAYER = 1
        self.COLLISION_TYPE_IMPASSABLE_TILE = 2
        self.MAX_COLLISION_TYPE = 2 # for adding more custom ones after

        # create player body and collision shape
        self.player_body = pymunk.Body(1, float('inf'))
        self.player_body.position = (self.player_spawn_point.x, self.player_spawn_point.y)
        player_shape = pymunk.Circle(self.player_body, 6)
        player_shape.collision_type = self.COLLISION_TYPE_PLAYER
        player_shape.elasticity = 0
        self.space.add(self.player_body, player_shape)

        # get all level tiles
        self.all_tiles = self.map.list_all_tiles()

        # create a collision square for each impassable tile
        for tile in self.all_tiles:
            if not tile['props'].get('passable', False):
                (tile_body, tile_shape) = self._make_tile_physics_body(tile['x'], tile['y'])
                tile_shape.collision_type = self.COLLISION_TYPE_IMPASSABLE_TILE
                tile_shape.elasticity = 0
                self.space.add(tile_body, tile_shape)
                tile['body'] = tile_body

        # load player character sprite frames
        player_spritesheet = pygame.image.load('../gfx/Sprout Lands - Sprites - premium pack/Characters/Basic Charakter Spritesheet.png').convert_alpha()
        self.player_frames = []
        for i in range(0, 4):
            frame = player_spritesheet.subsurface((16*(3*i + 1), 16, 16, 16))
            self.player_frames.append(frame)
        self.player_anim_framenum = 0

    def _make_tile_physics_body(self, x, y):
        tile_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        tile_body.position = (x*TILE_SIZE + TILE_SIZE/2, y*TILE_SIZE + TILE_SIZE/2)
        tile_shape = pymunk.Poly.create_box(tile_body, (TILE_SIZE, TILE_SIZE), 0.1)
        return (tile_body, tile_shape)

    def handle_input(self, keys, events, dt):
        # determine desired player velocity based on keyboard input
        player_desired_velo = Vec2()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_desired_velo += Vec2(-1, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_desired_velo += Vec2(1, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_desired_velo += Vec2(0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_desired_velo += Vec2(0, 1)

        # normalize and scale desired velocity
        if not player_desired_velo.is_zero():
            player_desired_velo = player_desired_velo.normalized() * PLAYER_SPEED

        # apply force to player body to make its velocity approach the desired velocity
        velocity_diff = player_desired_velo - Vec2(self.player_body.velocity[0], self.player_body.velocity[1])
        if dt > 0:
            movement_force = velocity_diff * (PLAYER_MOVEMENT_MAX_ACCEL * self.player_body.mass)
        else:
            movement_force = Vec2()
        self.player_body.apply_force_at_local_point((movement_force.x, movement_force.y))

        # update player sprite frame
        if player_desired_velo.is_zero():
            self.player_anim_framenum = 0
        else:
            if self.player_anim_framenum == 0:
                self.player_anim_framenum = 2
            elif self.player_anim_framenum == 2:
                self.player_anim_framenum = 3
            elif self.player_anim_framenum == 3:
                self.player_anim_framenum = 2
            else:
                assert False

    def advance_simulation(self, dt):
        self.space.step(dt)

    # returns new pygame surface, which will be scaled to fit the display
    def render(self):
        # render map to a temporary surface
        surface = self.map.render_map_to_new_surface()

        # render player sprite
        player_render_frame = self.player_frames[self.player_anim_framenum]
        player_render_pos = self.player_body.position - PLAYER_ANCHOR
        surface.blit(player_render_frame, (player_render_pos.x, player_render_pos.y))

        return surface

    def stop(self):
        pass
