import pygame
import pymunk
import time

from entity_base import BaseEntity
from player_state import player_state
from audio import get_audio
from entity_player import Player

def load():
    global assets
    assets = DoublerAssets()

class DoublerAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Sprout Lands - Sprites - premium pack/Objects/Mushrooms, Flowers, Stones.png').convert_alpha()
        self.sprite = spritesheet.subsurface((16, 0, 16, 16))
        self.anchor = (8, 13)

class Doubler(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=8, static=True)

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            new_player = Player(self.level, (self.body.position.x, self.body.position.y))
            self.level.entities.append(new_player)
            self.remove()

    def act(self, dt):
        pass
