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
        spritesheet = pygame.image.load('../gfx/2D Dungeon Asset Pack_v5.2/character and tileset/Dungeon_Enemy_v2.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 12))
        self.anchor = (8, 8)
        self.spritelist = []
        for i in range (0,1):
            frame = spritesheet.subsurface(((17*i +1), 0, 12, 15))
            self.spritelist.append(frame)

class ChargingMonster(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)
        self.timer = 0
        self.charging_velo = None

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
        
    def act(self, dt):
        self.timer += dt*4
        MAX_SPEED = 85
        MOVEMENT_STRENGTH = 15
        #player = self.get_nearest_player()
        #self.move_towards_charge_location(MAX_SPEED, MOVEMENT_STRENGTH)
        #dist = player.body.position.get_distance(self.body.position)
        if self.charging_velo is None:
            player = self.get_nearest_player()
            if player and player.body.position.get_distance(self.body.position) < 80:
                pos_diff = player.body.position - self.body.position
                self.charging_velo = pos_diff.normalized() * MAX_SPEED
            self.apply_force_to_achieve_velocity(Vec2d.zero(), MOVEMENT_STRENGTH)
        else:
            self.apply_force_to_achieve_velocity(self.charging_velo, MOVEMENT_STRENGTH)
        

