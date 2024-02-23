from level_dungeon import LevelDungeon
from level_dungeon_2 import LevelDungeon2
from level_lava_and_key import LevelLavaAndKey
from level_puzzle_room import LevelPuzzleRoom
from level_maze import LevelMaze

def load_levels():
    return [
        LevelDungeon(),
        LevelDungeon2(),
        LevelLavaAndKey(),
        LevelPuzzleRoom(),
        LevelMaze(),
    ]
