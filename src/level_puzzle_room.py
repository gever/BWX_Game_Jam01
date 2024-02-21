from audio import get_audio
from level_base import BaseLevel
from entity_skull_monster import SkullMonster
from entity_slime_monster import SlimeMonster
from collision_types import *

class DungeonLevel_PuzzleRoom(BaseLevel):
    def __init__(self):
        super().__init__('Puzzle_room.tmx')
        monster_spawn_point1 = self.map.get_object_by_name('monster_spawn1')
        monster_spawn_point2 = self.map.get_object_by_name('monster_spawn2')
        self.skull_monster1 = SkullMonster(self.space, (monster_spawn_point1.x, monster_spawn_point1.y))
        self.entities.append(self.skull_monster1)
        self.slime_monster1 = SlimeMonster(self.space, (monster_spawn_point2.x, monster_spawn_point2.y))
        self.entities.append(self.slime_monster1)
    
    def before_advance_simulation(self, dt):
        self.skull_monster1.move_towards_player(self.player)
        self.slime_monster1.move_towards_player(self.player)