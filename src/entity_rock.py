import pygame
import pymunk
import time
import random
from entity_base import BaseEntity
from player_state import player_state
from audio import get_audio

def load():
    global assets
    assets = RockAssets()

class RockAssets:
    def __init__(self):
    
        spritesheet1 = pygame.image.load('../gfx/Boulder.png').convert_alpha()
        self.sprite1 = spritesheet1.subsurface((0, 0, 32, 32))
            
        spritesheet2 = pygame.image.load('../gfx/Boulder02.png').convert_alpha()
        self.sprite2 = spritesheet2.subsurface((0, 0, 32, 32))
        self.anchor = (17, 15)

class Rock(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=13, static=True,square=True)
        self.touch_time = None
        self.beinghit = False 
        self.sprite_picker = random.randint(0,1)
        if self.sprite_picker == 0:
            self.sprite = assets.sprite1
        else:
            self.sprite = assets.sprite2

    def get_render_info(self):
        return {
            'sprite': self.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            if not self.beinghit:
                if player_state.inventory_contains('pickaxe'):
                    # drop/break the pickaxe
                    
                    get_audio().play_sfx('mine_rock')
                    self.touch_time = time.time()
                    self.beinghit = True

    def act(self, dt):
        if self.touch_time:
            if time.time() - self.touch_time >= 1:
                pickaxe = player_state.get_item('pickaxe')
                pickaxe.dropped() # TODO: animate this
                self.remove()