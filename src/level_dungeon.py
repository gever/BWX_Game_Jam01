import pygame
import pymunk

from audio import get_audio
from level import BaseLevel

class SkullMonsterCreator:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/2D Dungeon Asset Pack_v5.2/character and tileset/Dungeon_Enemy_v2.png').convert_alpha()
        self.sprite = spritesheet.subsurface((32, 0, 16, 16))
        self.anchor = (8, 14)

    def create(self, space, initial_pos):
        return SkullMonster(self, space, initial_pos)

class SkullMonster:
    def __init__(self, creator, space, initial_pos):
        self.sprite = creator.sprite
        self.anchor = creator.anchor
        self.space = space

        self.body = pymunk.Body(1, float('inf'))
        self.body.position = initial_pos
        self.shape = pymunk.Circle(self.body, 6)
        # self.shape.collision_type = self.COLLISION_TYPE_PLAYER
        self.shape.elasticity = 0
        space.add(self.body, self.shape)

    def get_render_info(self):
        return {
            'sprite': self.sprite,
            'pos': self.body.position,
            'anchor': self.anchor,
        }

class DungeonLevel(BaseLevel):
    def __init__(self):
        super().__init__('dungeon_map.tmx')

        self.COLLISION_TYPE_BLUE_LIGHT = self.MAX_COLLISION_TYPE + 1

        for tile in self.all_tiles:
            if tile['props']['id'] == 65:
                (tile_body, tile_shape) = self._make_tile_physics_body(tile['x'], tile['y'])
                tile_shape.collision_type = self.COLLISION_TYPE_BLUE_LIGHT
                tile_shape.sensor = True
                self.space.add(tile_body, tile_shape)
                handler = self.space.add_collision_handler(self.COLLISION_TYPE_PLAYER, self.COLLISION_TYPE_BLUE_LIGHT)
                handler.begin = self.handle_blue_light_collision

        # add monster
        monster_spawn_point = self.map.get_object_by_name('monster_spawn')
        skull_monster_creator = SkullMonsterCreator()
        self.skull_monster = skull_monster_creator.create(self.space, (monster_spawn_point.x, monster_spawn_point.y))
        self.extra_renderables.append(self.skull_monster)

    def handle_blue_light_collision(self, arbiter, space, data):
        get_audio().play_sfx('rasp')
        return True

    def before_advance_simulation(self, dt):
        # make skull monster move towards player
        MAX_SPEED = 50
        MAX_ACCEL = 10
        player_pos = self.player_body.position
        monster_pos = self.skull_monster.body.position
        pos_diff = player_pos - monster_pos
        if pos_diff.length > 0:
            desired_velocity = pos_diff.normalized() * MAX_SPEED
        else:
            desired_velocity = pymunk.Vec2d(0, 0)
        self._apply_force_to_achieve_velocity(self.skull_monster.body, desired_velocity, MAX_ACCEL)
