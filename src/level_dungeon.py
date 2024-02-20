from audio import get_audio
from level import BaseLevel

class DungeonLevel(BaseLevel):
    def __init__(self):
        super().__init__('dungeon_map.tmx')

    def start(self):
        super().start()

        self.COLLISION_TYPE_BLUE_LIGHT = self.MAX_COLLISION_TYPE + 1

        for tile in self.all_tiles:
            if tile['props']['id'] == 65:
                (tile_body, tile_shape) = self._make_tile_physics_body(tile['x'], tile['y'])
                tile_shape.collision_type = self.COLLISION_TYPE_BLUE_LIGHT
                tile_shape.sensor = True
                self.space.add(tile_body, tile_shape)
                handler = self.space.add_collision_handler(self.COLLISION_TYPE_PLAYER, self.COLLISION_TYPE_BLUE_LIGHT)
                handler.begin = self.handle_blue_light_collision

    def handle_blue_light_collision(self, arbiter, space, data):
        get_audio().play_sfx('rasp')
        return True
