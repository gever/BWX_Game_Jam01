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
        left_spritesheet = pygame.image.load('../gfx/Beetle.png').convert_alpha()
        left_spritelist = []
        for i in [0,1]:
            frame = left_spritesheet.subsurface(((30*i), 0, 30, 16))
            left_spritelist.append(frame)

        right_spritelist = left_spritelist.copy()
        right_spritesheet = pygame.image.load('../gfx/beetle pointing left.png').convert_alpha()
        right_spritelist = []
        for i in [0,1]:
            frame = right_spritesheet.subsurface(((30*i) + 3, 0, 30, 16))
            right_spritelist.append(frame)

        self.anchor = (18,  9)

        self.anims = {
            'left': left_spritelist,
            'right': right_spritelist,
        }

class ChargingMonster(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=10)
        self.timer = 0
        self.charging_velo = None
        self.chasing = False
        self.timertillpause = 1.5
        self.timepaused = None
        self.current_anim = 'right'

    def get_render_info(self):
        anim = assets.anims[self.current_anim]
        frame = int(self.timer) % 2
        return {
            'sprite': anim[frame],
            'pos': self.body.position,
            'anchor': assets.anchor,
        }
    def handle_entity_collision(self, other_entity):
        if other_entity.is_player():
            other_entity.kill()
        if isinstance(other_entity, Rock):
            other_entity.remove()

    def handle_tile_collision(self):
        self.charging_velo = None
        self.timertillpause = -1

    def act(self, dt):
        self.current_anim = 'right' if (self.body.velocity.x > 0) else 'left'
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


