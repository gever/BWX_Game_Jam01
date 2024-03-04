import pygame
import pymunk

from entity_base import BaseEntity
from entity_waterblob import WaterBlob

def load():
    global assets
    assets = LavaBlobAssets()

class LavaBlobAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Lava Blob.png').convert_alpha()
        paused_spritesheet = pygame.image.load('../gfx/Half Stone Lava Blob.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 12))
        self.pausedsprite = paused_spritesheet.subsurface((0, 0, 16, 12))
        self.spritelist = []
        for i in range (0,4):
            frame = spritesheet.subsurface(((20*i), 0, 16, 12))
            self.spritelist.append(frame)
        self.anchor = (8, 14)

class LavaBlob(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)
        self.chasing = False
        self.time_until_death = 2.5
        self.paused = False
        self.less_speed = 0
        self.timer = 0

    def get_render_info(self):
        frame = int(self.timer) % len(assets.spritelist)
        return {
            'sprite': assets.pausedsprite if self.paused else assets.spritelist[frame],
            'pos': self.body.position,
            'anchor': assets.anchor,
        }
    
    def handle_entity_collision(self, other_entity):
        if not self.paused:
            # TODO: trigger player death noise
            if other_entity.is_player():
                other_entity.remove()
                return

            # TODO: trigger water blob death noise
            if isinstance(other_entity, WaterBlob):
                other_entity.remove()

    def act(self,dt):
        self.timer += dt*7
        MAX_SPEED = 85
        MOVEMENT_STRENGTH = 15
        player = self.get_nearest_player()


        tile_props = self.get_current_tile_props()
        if tile_props and tile_props.get('water'):
            self.paused = True

        tile_props = self.get_current_tile_props()
        if tile_props and tile_props.get('kills you'):
            if self.paused == True:
                self.paused = False
                self.time_until_death = 2.5
        
        if player:
            dist = player.body.position.get_distance(self.body.position)
            if dist < 80:
               self.chasing = True

            if self.paused == True:
                MAX_SPEED = 0
                MOVEMENT_STRENGTH = 25
                self.chasing = False

            else:
                MAX_SPEED = 85
                MOVEMENT_STRENGTH = 15

            if self.chasing == True:
                    self.move_towards_player(MAX_SPEED, MOVEMENT_STRENGTH)
                    self.time_until_death -= dt
                    if self.time_until_death <0:
                        self.paused = True
                        
            else:
                self.body.velocity = (0,0)