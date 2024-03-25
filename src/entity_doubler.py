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
            # by default, spawn new player at the same position as the doubler
            spawn_pos = (self.body.position.x, self.body.position.y)

            # is there another doubler?
            other_doubler = None
            for entity in self.level.entities:
                if isinstance(entity, Doubler) and entity != self:
                    other_doubler = entity
            if other_doubler:
                other_doubler.remove()
                spawn_pos = (other_doubler.body.position.x, other_doubler.body.position.y)

            get_audio().play_sfx('doubler')
            get_audio().play_sfx('eating')

            new_player = Player(self.level, spawn_pos)
            self.level.entities.append(new_player)
            self.remove()

    def act(self, dt):
        pass
