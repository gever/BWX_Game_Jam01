import os
import random

import pygame
import pymunk

from audio import get_audio
from config import *
from pygame import event
from pygame import key
from collision_types import *
from map import TiledMap
from entity_player import Player
from entities_loader import ENTITY_MAP
from player_state import player_state
from lighting import create_light_surface
from entity_particle_lava import LavaParticle

class BaseLevel:
    def __init__(self, map_fn):
        self.map_fn = map_fn

        # load Tiled map
        self.map = TiledMap(os.path.join('../maps', map_fn))
        self.heart_sprite = pygame.image.load('../gfx/Heart.png').convert_alpha()
        self.reset()

        self.reset_queued = False

    # override in derived class to do something extra when the level is reset
    def reset_extra(self):
        pass

    def reset(self):
        self.entities = []

        # find player spawn point
        self.player_spawn_point = self.map.get_object_by_name('player_spawn')
        assert self.player_spawn_point, 'No player spawn found in map: %s' % self.map_fn

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

        self.reset_extra()

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
            self.reset_queued = True

    def level_complete(self):
        for obj in self.map.list_all_objects():
            if obj.name == 'level_exit':
                any_player_near_exit = False
                for entity in self.entities:
                    if entity.is_player():
                        player_position = entity.body.position
                        distance = player_position.get_distance((obj.x, obj.y))
                        if distance <= 10:
                            any_player_near_exit = True
                            break
                if not any_player_near_exit:
                    return False
        return True

    def get_seeing_double(self):
        player_count = 0
        for entity in self.entities:
            if entity.is_player():
                player_count += 1
        return player_count > 1

    def _make_tile_physics_body(self, coords):
        (x, y) = coords
        tile_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        tile_body.position = (x*TILE_SIZE + TILE_SIZE/2, y*TILE_SIZE + TILE_SIZE/2)
        tile_shape = pymunk.Poly.create_box(tile_body, (TILE_SIZE, TILE_SIZE), 0.1)
        return (tile_body, tile_shape)

    def handle_input(self, keys, events, dt):
        for entity in self.entities:
            entity.handle_input(keys, events, dt)

    def is_start_level(self):
        return False

    # override this in a derived class to do something extra before the simulation step
    def extra_advance_simulation(self, dt):
        pass

    def advance_simulation(self, dt):
        for entity in self.entities:
            entity.act(dt)

        for tile in self.visible_tiles:
            if tile['props'] and tile['props'].get('kills you'):
                # should be lava
                if random.random() < 0.01:
                    particle = LavaParticle(self, (tile['x']*TILE_SIZE + TILE_SIZE/2, tile['y']*TILE_SIZE + TILE_SIZE/2), (random.uniform(-50, 50), random.uniform(-100, 0)))
                    self.entities.append(particle)

        self.extra_advance_simulation(dt)

        self.space.step(dt)

        if self.reset_queued:
            self.reset()
            self.reset_queued = False

    def render_entities(self, surface):
        render_infos = [entity.get_render_info() for entity in self.entities]
        for info in render_infos:
            render_pos = (info['pos'][0] - info['anchor'][0], info['pos'][1] - info['anchor'][1])
            info['render_pos'] = render_pos

        # sort by y position so that entities are drawn in the correct order
        render_infos.sort(key=lambda info: info['pos'][1])

        # render all entities
        for info in render_infos:
            surface.blit(info['sprite'], info['render_pos'])

    # returns new pygame surface, which will be scaled to fit the display
    def render(self, apply_lighting=True):
        # render map to a temporary surface
        surface = self.map.render_map_to_new_surface()

        self.render_entities(surface)

        # render lighting
        if apply_lighting:
            lights = []

            for entity in self.entities:
                radius = entity.get_lighting()
                offset = entity.get_lighting_offset()
                if radius is not None:
                    lights.append({
                        'x': entity.body.position.x + offset[0],
                        'y': entity.body.position.y + offset[1],
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
            live_counter = player_state.total_lives
            lives_offset = 0
            for lives in range(live_counter):
                surface.blit(self.heart_sprite, (lives_offset, 0))
                lives_offset += 16
        return surface

    def stop(self):
        pass
