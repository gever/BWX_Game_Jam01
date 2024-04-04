import pygame
import pymunk

from player_state import player_state
from audio import get_audio
from level_base import BaseLevel
from collision_types import COLLISION_TYPE_IMPASSABLE_TILE

class Level(BaseLevel):
    def __init__(self, map_fn):
        super().__init__(map_fn)

        self.lose_image = pygame.image.load('../gfx/game_over.png').convert_alpha()
        self.win_image = pygame.image.load('../gfx/end_screen.png').convert_alpha()

    def is_end_level(self):
        return True
    
    def render(self, apply_lighting):
        # render map to a temporary surface
        surface = self.map.render_map_to_new_surface()
        if player_state.total_lives >= 1:
            surface.blit(self.win_image, (0, 0))
        else:
            surface.blit(self.lose_image, (0, 0))

        self.render_entities(surface)

        return surface