import os

from level_base import BaseLevel

def load_levels():
    # list .tmx files in maps dir
    sorted_map_fns = []
    for fn in os.listdir('../maps'):
        if fn.endswith('.tmx'):
            sorted_map_fns.append(fn)
    sorted_map_fns.sort()

    levels = []
    for fn in sorted_map_fns:
        print('loading map:', fn)
        full_fn = os.path.join('../maps', fn)

        levels.append(BaseLevel(full_fn))

    return levels

    # return [
    #     LevelButtonAndBridge(),
    #     LevelLavaAndKey(),
    #     LevelDungeon(),
    #     LevelDungeon2(),
    #     LevelPuzzleRoom(),
    #     LevelMaze(),
    # ]
