import pygame
import pymunk

from audio import get_audio
from level_base import BaseLevel
from entity_skull_monster import SkullMonster
from collision_types import *
from player_state import player_state

class LevelDungeon(BaseLevel):
    def __init__(self):
        super().__init__('dungeon_map.tmx')

        self.COLLISION_TYPE_BLUE_LIGHT = get_new_collision_type_id()
        for tile in self.visible_tiles:
            if tile['props']['id'] == 65:
                (tile_body, tile_shape) = self._make_tile_physics_body((tile['x'], tile['y']))
                tile_body.entity_name = 'blue_light'
                tile_shape.collision_type = self.COLLISION_TYPE_BLUE_LIGHT
                tile_shape.sensor = True
                self.space.add(tile_body, tile_shape)
                handler = self.space.add_collision_handler(COLLISION_TYPE_ENTITY, self.COLLISION_TYPE_BLUE_LIGHT)
                handler.begin = self.handle_blue_light_collision

    def handle_blue_light_collision(self, arbiter, space, data):
        get_audio().play_sfx('rasp')
        player_state.apply_damage()
        for shape in arbiter.shapes:
            if hasattr(shape.body, 'entity_name'):
                print(shape.body.entity_name)
            else:
                print('no entity_name')
        return True
