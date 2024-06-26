import pygame
import pymunk 

from entity_base import BaseEntity
from player_state import player_state

def load():
    global assets
    assets = PickaxeAssets()

class PickaxeAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Pickaxe.png').convert_alpha()
        self.sprite = spritesheet.subsurface((0, 0, 16, 16))
        self.sprite_left = pygame.transform.flip(self.sprite, True, False)
        self.broken_sprite = spritesheet.subsurface((16, 0, 16, 16))
        self.anchor = (8, 8)

class Pickaxe(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, radius=4, static=True, sensor=True)
        self.carrier = None
        self.broken = False
    def get_render_info(self):
        if self.carrier:
            if self.carrier.facing == self.carrier.FACING_L:
                return {
                    'sprite': assets.sprite_left,
                    'pos': self.body.position,
                    'anchor': assets.anchor,
                }
        return {
            'sprite': assets.broken_sprite if self.broken else assets.sprite,
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    # update pick position to match player
    def act(self, dt):
        if self.carrier:
            if self.carrier.facing == self.carrier.FACING_R:
                self.body.position = (self.carrier.body.position.x+8, self.carrier.body.position.y-6)
            elif self.carrier.facing == self.carrier.FACING_L:
                self.body.position = (self.carrier.body.position.x-8, self.carrier.body.position.y-6)
            else:
                self.body.position = (self.carrier.body.position.x+8, self.carrier.body.position.y-6)


    def handle_entity_collision(self, other_entity):
        if other_entity.is_player() and not self.broken and not player_state.inventory_contains('pickaxe'):
            self.carrier = other_entity
            player_state.add_to_inventory('pickaxe', self)

    def dropped(self):
        if self.carrier:
            px, py = self.carrier.body.position
            #self.body.position = (px-(vx/5), py-(vy/5))
            if self.carrier.facing == self.carrier.FACING_R:
                self.body.position = (px - 12, py)
            if self.carrier.facing == self.carrier.FACING_L:
                self.body.position = (px + 12, py)
            self.carrier = None
            player_state.remove_from_inventory('pickaxe')
            self.broken = True
