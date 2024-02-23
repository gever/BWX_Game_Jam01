from level_dungeon import LevelDungeon
from level_dungeon_2 import LevelDungeon2
from level_lava_and_key import LevelLavaAndKey
from level_puzzle_room import LevelPuzzleRoom
from level_maze import LevelMaze
from level_button_and_bridge import LevelButtonAndBridge

def load_levels():
    return [
        LevelButtonAndBridge(),
        LevelLavaAndKey(),
        LevelDungeon(),
        LevelDungeon2(),
        LevelPuzzleRoom(),
        LevelMaze(),
    ]
