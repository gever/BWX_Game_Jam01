import pygame
import pymunk
import time

from entity_base import BaseEntity
from player_state import player_state
from audio import get_audio

def load():
    global assets
    assets = RockAssets()

class RockAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Boulder.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 32, 32))
        self.anchor = (17, 15)

class Rock(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=13, static=True,square=True)
        self.touch_time = None

    def get_render_info(self):
        return {
            'sprite': assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            if player_state.inventory_contains('pickaxe'):
                # drop/break the pickaxe
                
                get_audio().play_sfx('mine_rock')
                self.touch_time = time.time()

    def act(self, dt):
        if self.touch_time:
            if time.time() - self.touch_time >= 1:
                pickaxe = player_state.get_item('pickaxe')
                pickaxe.dropped() # TODO: animate this
                self.remove()