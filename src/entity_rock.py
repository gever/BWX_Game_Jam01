import pygame
import pymunk
import time
import random
from entity_base import BaseEntity
from player_state import player_state
from audio import get_audio
from entity_particle_rock import RockParticle

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
        self.sprite_picker = random.randint(0,1)
        self.hits = 0
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
            if player_state.inventory_contains('pickaxe'):
                self.hits += 1

                if self.hits >= 3:
                    self.remove()
                    pickaxe = player_state.get_item('pickaxe')
                    if pickaxe == None:
                        return
                    pickaxe.dropped() # TODO: animate this
                    for i in range(50):
                        particle = RockParticle(self.level, self.body.position, (random.uniform(-50, 50), random.uniform(-100, 0)))
                        self.level.entities.append(particle)
                    self.remove()

                    get_audio().play_sfx('mine_rock')
                    
    def act(self, dt):
        pass
        #if self.touch_time:
            #if time.time() - self.touch_time >= 1:
            #    pickaxe = player_state.get_item('pickaxe')
            #    if pickaxe == None:
            #        return
            #    pickaxe.dropped() # TODO: animate this
            #    for i in range(50):
            #        particle = RockParticle(self.level, self.body.position, (random.uniform(-50, 50), random.uniform(-100, 0)))
            #        self.level.entities.append(particle)
            #    self.remove()

