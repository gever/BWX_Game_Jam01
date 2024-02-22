import os

import pygame
import pymunk

from audio import get_audio
from config import *
from collision_types import *
from map import TiledMap
from entity_player import Player

class BaseLevel:
    def __init__(self, map_fn):
        # load Tiled map
        self.map = TiledMap(os.path.join('../maps', map_fn))

        self.entities = []

        # find player spawn point
        self.player_spawn_point = self.map.get_object_by_name('player_spawn')

        self.exit_point = self.map.get_object_by_name('level_exit')

        # create physics space
        self.space = pymunk.Space()

        # create player
        self.player = Player(self.space, (self.player_spawn_point.x, self.player_spawn_point.y))
        self.entities.append(self.player)

        # get all level tiles
        self.all_tiles = self.map.list_all_tiles()

        # create a collision square for each impassable tile
        for tile in self.all_tiles:
            if not tile['props'].get('passable', False):
                (tile_body, tile_shape) = self._make_tile_physics_body(tile['x'], tile['y'])
                tile_shape.collision_type = COLLISION_TYPE_IMPASSABLE_TILE
                tile_shape.elasticity = 0
                self.space.add(tile_body, tile_shape)
                tile['body'] = tile_body

    def start(self):
        pass

    def stop(self):
        pass

    def _make_tile_physics_body(self, x, y):
        tile_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        tile_body.position = (x*TILE_SIZE + TILE_SIZE/2, y*TILE_SIZE + TILE_SIZE/2)
        tile_shape = pymunk.Poly.create_box(tile_body, (TILE_SIZE, TILE_SIZE), 0.1)
        return (tile_body, tile_shape)

    def handle_input(self, keys, events, dt):
        for entity in self.entities:
            entity.handle_input(keys, events, dt)

    def before_advance_simulation(self, dt):
        # override this in a derived class to do something before the simulation step, e.g. monster logic
        pass

    def advance_simulation(self, dt):
        self.before_advance_simulation(dt)
        self.space.step(dt)

    # returns new pygame surface, which will be scaled to fit the display
    def render(self):
        # render map to a temporary surface
        surface = self.map.render_map_to_new_surface()

        # render all entities
        for entity in self.entities:
            render_info = entity.get_render_info()
            render_pos = (render_info['pos'][0] - render_info['anchor'][0], render_info['pos'][1] - render_info['anchor'][1])
            surface.blit(render_info['sprite'], render_pos)

        return surface

    def stop(self):
        pass
