import pygame
import pymunk

from entity_base import BaseEntity

def load():
    global assets
    assets = LavaBlobAssets()

class LavaBlobAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Lava Blob.png').convert_alpha()
        paused_spritesheet = pygame.image.load('../gfx/Stone Lava Blob.png').convert_alpha()
        self.sprite = spritesheet.subsurface((17, 20, 16, 12))
        self.pausedsprite = paused_spritesheet.subsurface((17, 20, 16, 12))
        self.anchor = (8, 14)

class LavaBlob(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)
        self.chasing = False
        self.time_until_death = 2.5
        self.paused = False

    def get_render_info(self):
        return {
            'sprite': assets.pausedsprite if self.paused else assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }
    
    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            if not self.paused:
                other_entity.remove()

    def act(self,dt):
        MAX_SPEED = 85
        MOVEMENT_STRENGTH = 15
        player = self.get_nearest_player()
        
        if player:
            dist = player.body.position.get_distance(self.body.position)
            if dist < 80:
               self.chasing = True

            if self.chasing == True:
                if self.paused == False:
                    self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)
                    self.time_until_death -= dt
                    if self.time_until_death <0:
                        self.paused = True
                        
                else:
                    self.chasing = False
                    self.body.velocity = (0,0)
            else:
                self.body.velocity = (0,0)


