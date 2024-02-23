from audio import get_audio
from level_base import BaseLevel
from entity_skull_monster import SkullMonster
from entity_slime_monster import SlimeMonster
from collision_types import *

class LevelMaze(BaseLevel):
    def __init__(self):
        super().__init__('Maze.tmx')
