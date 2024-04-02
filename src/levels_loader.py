import os

from map import TiledMap

from level_base import BaseLevel

def load_levels():
    # list .tmx files in maps dir
    sorted_map_fns = []
    for fn in os.listdir('../maps'):
        if fn.endswith('.tmx'):
            sorted_map_fns.append(fn)
    sorted_map_fns.sort()

    levels = []
    for map_fn in sorted_map_fns:
        print('loading map:', map_fn)

        # load one copy of the map just to look at its properties,
        # to see if we want to actually load it with a subclass.
        # this seems inefficient but is not a big deal.
        temp_map = TiledMap(os.path.join('../maps', map_fn))
        subclass_name = temp_map.tmx_data.properties.get('subclass')
        current_level = None
        if subclass_name:
            imp = __import__(subclass_name, globals(), locals(), ['Level'], 0)
            Level = getattr(imp, 'Level')
            print('map %r has subclass %r' % (map_fn, subclass_name))
            current_level = Level(map_fn)
        else:
            current_level = BaseLevel(map_fn)
        levels.append( current_level )
        current_level.filename = map_fn

    return levels
