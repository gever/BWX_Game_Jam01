import os

from map import TiledMap

from level_base import BaseLevel

def check_for_reset():
    map_fns = []
    for fn in os.listdir('../maps'):
        if fn.endswith('.tmx'):
            map_fns.append(fn)

    for map_fn in map_fns:
        if map_fn == 'game over.tmx':
            print('game over')
