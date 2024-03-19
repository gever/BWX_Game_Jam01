import pygame
import pymunk
from pymunk import Vec2d

from entity_rock import Rock
from entity_base import BaseEntity

def load():
    global assets
    assets = ChargingMonsterAssets()

class ChargingMonsterAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Beetle.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 64, 16))
        self.anchor = (8, 8)
        self.spritelist = []
        for i in [0,1]:
            frame = spritesheet.subsurface(((30*i), 0, 30, 16))
            self.spritelist.append(frame)

class ChargingMonster(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)
        self.timer = 0
        self.charging_velo = None
        self.chasing = False
        self.timertillpause = 1.5
        self.timepaused = None

    def get_render_info(self):
        frame = int(self.timer) % len(assets.spritelist)
        return {
            'sprite': assets.spritelist[frame],
            'pos': self.body.position,
            'anchor': assets.anchor,
        }
    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            other_entity.remove()
            return
        if isinstance(other_entity, Rock):
            other_entity.remove()
    
    def handle_tile_collision(self):
        self.charging_velo = None
        self.timertillpause = -1
        self.die_if_tile_kills_you()
        
    def act(self, dt):
        self.timer += dt*4
        MAX_SPEED = 150
        MOVEMENT_STRENGTH = 7
        if not self.timepaused:
            if self.charging_velo is None:
                player = self.get_nearest_player()
                if player and player.body.position.get_distance(self.body.position) < 150 or self.chasing:
                    self.chasing = True
                    pos_diff = player.body.position - self.body.position
                    self.charging_velo = pos_diff.normalized() * MAX_SPEED
                self.apply_force_to_achieve_velocity(Vec2d.zero(), MOVEMENT_STRENGTH)
            else:
                self.apply_force_to_achieve_velocity(self.charging_velo, MOVEMENT_STRENGTH)
                self.timertillpause -=dt
                if self.timertillpause < 0:
                    self.timertillpause = 1.5
                    self.charging_velo = None
                    self.timepaused = .5
        else:
            self.timepaused -= dt
            self.apply_force_to_achieve_velocity(Vec2d.zero(), MOVEMENT_STRENGTH)
            if self.timepaused < 0:
                self.timepaused = None
        

