import pygame
import pymunk

from audio import get_audio
from level_base import BaseLevel
from entity_skull_monster import SkullMonster
from collision_types import *
from player_state import player_state

class DungeonLevel(BaseLevel):
    def __init__(self):
        super().__init__('dungeon_map.tmx')

        self.COLLISION_TYPE_BLUE_LIGHT = get_new_collision_type_id()
        for tile in self.all_tiles:
            if tile['props']['id'] == 65:
                (tile_body, tile_shape) = self._make_tile_physics_body(tile['x'], tile['y'])
                tile_shape.collision_type = self.COLLISION_TYPE_BLUE_LIGHT
                tile_shape.sensor = True
                self.space.add(tile_body, tile_shape)
                handler = self.space.add_collision_handler(COLLISION_TYPE_PLAYER, self.COLLISION_TYPE_BLUE_LIGHT)
                handler.begin = self.handle_blue_light_collision

        # add monster
        monster_spawn_point = self.map.get_object_by_name('monster_spawn')
        self.skull_monster = SkullMonster(self.space, (monster_spawn_point.x, monster_spawn_point.y))
        self.entities.append(self.skull_monster)

        self.skull_monster2 = SkullMonster(self.space, (monster_spawn_point.x - 50, monster_spawn_point.y))
        self.entities.append(self.skull_monster2)

    def handle_blue_light_collision(self, arbiter, space, data):
        get_audio().play_sfx('rasp')
        player_state.apply_damage()
        return True

    def before_advance_simulation(self, dt):
        self.skull_monster.move_towards_player(self.player)
        self.skull_monster2.move_towards_player(self.player)
