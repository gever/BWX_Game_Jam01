from level_dungeon import DungeonLevel
from level_dungeon_2 import DungeonLevel2
from level_lava_and_key import DungeonLevel_LavaAndKey
from level_puzzle_room import DungeonLevel_PuzzleRoom
from level_maze import DungeonLevel_Maze

def load_levels():
    return [
        DungeonLevel(),
        DungeonLevel2(),
        DungeonLevel_LavaAndKey(),
        DungeonLevel_PuzzleRoom(),
        DungeonLevel_Maze(),
    ]
