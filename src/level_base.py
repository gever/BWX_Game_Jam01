import os

import pygame
import pymunk

from audio import get_audio
from config import *
from collision_types import *
from map import TiledMap
from entity_player import Player
from entities_loader import ENTITY_MAP
from player_state import player_state
from lighting import create_light_surface

class BaseLevel:
    def __init__(self, map_fn):
        self.map_fn = map_fn

        # load Tiled map
        self.map = TiledMap(os.path.join('../maps', map_fn))

        self.reset()

    def reset(self):
        self.entities = []

        # find player spawn point
        self.player_spawn_point = self.map.get_object_by_name('player_spawn')
        assert self.player_spawn_point, 'No player spawn found in map: %s' % self.map_fn

        self.exit_point = self.map.get_object_by_name('level_exit')
        assert self.exit_point, 'No level exit found in map: %s' % self.map_fn

        # create physics space
        self.space = pymunk.Space()

        # add collision handlers
        entity_entity_collision_handler = self.space.add_collision_handler(COLLISION_TYPE_ENTITY, COLLISION_TYPE_ENTITY)
        entity_entity_collision_handler.begin = self._handle_entity_entity_collision

        entity_tile_collision_handler = self.space.add_collision_handler(COLLISION_TYPE_ENTITY, COLLISION_TYPE_IMPASSABLE_TILE)
        entity_tile_collision_handler.begin = self._handle_entity_tile_collision

        # create tile physicspython game.py
        self.tile_physics_objs = [] # both bodies and shapes
        self._create_tile_physics()

        # create entities (including player) for each object in the map with a matching name
        for obj in self.map.list_all_objects():
            if obj.name in ENTITY_MAP:
                entity = ENTITY_MAP[obj.name](self, (obj.x, obj.y))
                self.entities.append(entity)

        player_state.reset()

    def _handle_entity_entity_collision(self, arbiter, space, data):
        if hasattr(arbiter.shapes[0].body, 'entity') and hasattr(arbiter.shapes[1].body, 'entity'):
            entity1 = arbiter.shapes[0].body.entity
            entity2 = arbiter.shapes[1].body.entity
            entity1.handle_entity_collision(entity2)
            entity2.handle_entity_collision(entity1)
        return True

    def _handle_entity_tile_collision(self, arbiter, space, data):
        if hasattr(arbiter.shapes[0].body, 'entity'):
            entity = arbiter.shapes[0].body.entity
            entity.handle_tile_collision()
        return True

    def _create_tile_physics(self):
        # if we have already created tile physics, remove them
        for phys_obj in self.tile_physics_objs:
            self.space.remove(phys_obj)
        self.tile_physics_objs = []

        self.visible_tiles = self.map.list_visible_tiles()

        # create a collision square for each impassable tile
        for tile in self.visible_tiles:
            # if tile.get('props') and tile['props'].get('colliders'):
            #     colliders = tile['props']['colliders']
            #     for collider in colliders:
            #         print('collider:', collider.points)
            if tile['props'] and (not tile['props'].get('passable', True)):
                tile_coords = (tile['x'], tile['y'])
                (tile_body, tile_shape) = self._make_tile_physics_body(tile_coords)
                tile_shape.collision_type = COLLISION_TYPE_IMPASSABLE_TILE
                tile_shape.elasticity = 0
                self.space.add(tile_body, tile_shape)
                self.tile_physics_objs.append(tile_body)
                self.tile_physics_objs.append(tile_shape)

    def _get_tile_props_by_coords(self, x, y):
        return self.map.get_tile_props_by_coords(self.map.get_first_tile_layer_index(), x, y)

    def start(self):
        pass

    def stop(self):
        pass

    def remove_entity(self, entity):
        self.entities.remove(entity)

        # if there are no more players, the level is over
        if not any([entity.is_player() for entity in self.entities]):
            self.reset()

    def level_complete(self):
        for entity in self.entities:
            if entity.is_player():
                player_position = entity.body.position
                distance = player_position.get_distance((self.exit_point.x, self.exit_point.y))
                if distance <= 10:
                    return True
        return False

    def _make_tile_physics_body(self, coords):
        (x, y) = coords
        tile_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        tile_body.position = (x*TILE_SIZE + TILE_SIZE/2, y*TILE_SIZE + TILE_SIZE/2)
        tile_shape = pymunk.Poly.create_box(tile_body, (TILE_SIZE, TILE_SIZE), 0.1)
        return (tile_body, tile_shape)

    def handle_input(self, keys, events, dt):
        for entity in self.entities:
            entity.handle_input(keys, events, dt)

    def before_advance_simulation(self, dt):
        # override this in a derived class to do something extra before the simulation step
        for entity in self.entities:
            entity.act(dt)

    def advance_simulation(self, dt):
        self.before_advance_simulation(dt)
        self.space.step(dt)

    # returns new pygame surface, which will be scaled to fit the display
    def render(self, apply_lighting=True):
        # render map to a temporary surface
        surface = self.map.render_map_to_new_surface()

        render_infos = [entity.get_render_info() for entity in self.entities]
        for info in render_infos:
            render_pos = (info['pos'][0] - info['anchor'][0], info['pos'][1] - info['anchor'][1])
            info['render_pos'] = render_pos

        # sort by y position so that entities are drawn in the correct order
        render_infos.sort(key=lambda info: info['pos'][1])

        # render all entities
        for info in render_infos:
            surface.blit(info['sprite'], info['render_pos'])

        # render lighting
        if apply_lighting:
            lights = []

            for entity in self.entities:
                radius = entity.get_lighting()
                if radius is not None:
                    lights.append({
                        'x': entity.body.position.x,
                        'y': entity.body.position.y,
                        'r': radius,
                    })

            for tile in self.visible_tiles:
                if tile['props'] and tile['props'].get('light'):
                    lights.append({
                        'x': tile['x'] * TILE_SIZE + TILE_SIZE/2,
                        'y': tile['y'] * TILE_SIZE + TILE_SIZE/2,
                        'r': tile['props']['light'],
                    })

            light_surface = create_light_surface(surface.get_width(), surface.get_height(), lights)
            surface.blit(light_surface, (0, 0), special_flags=pygame.BLEND_MULT)

        return surface

    def stop(self):
        pass
