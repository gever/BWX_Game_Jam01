from audio import get_audio
from level import BaseLevel

class DungeonLevel2(BaseLevel):
    def __init__(self):
        super().__init__('dungeon_map_2.tmx')

    def start(self):
        super().start()
