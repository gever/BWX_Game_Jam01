import pygame
import pymunk
import time
import random

from audio import get_audio
from config import *
from entity_base import BaseEntity
from vec2 import Vec2
from player_state import player_state
from entity_particle_water import WaterParticle

def load():
    global assets
    assets = PlayerAssets()

class PlayerAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/miner_walk_cycle.png').convert_alpha()
        swim_spritesheet = pygame.image.load('../gfx/Swimming_player_sprite.png').convert_alpha()
        death_player_spritesheet = pygame.image.load('../gfx/Dead_Player.png').convert_alpha()
        sprites = []
        swim_sprites = []
        dead_sprites = []
        for i in range(0, 4):
            frame = spritesheet.subsurface((16*i, 0, 16, 22))
            sprites.append(frame)
        self.anims = {
            'left': sprites[2:4],
            'right': sprites[0:2],
        }
        for i in range(0, 2):
            swim_frames = swim_spritesheet.subsurface(((17*i + 1), 1, 16, 35))
            swim_sprites.append(swim_frames)
        self.swim_anims = {
            'swim_left': swim_sprites[0:1],
            'swim_right': swim_sprites[1:2],
        }
        for i in range(0, 1):
            dead_frames = death_player_spritesheet.subsurface((0, 1, 24, 16))
            dead_sprites.append(dead_frames)
        self.dead_anims = {
            'dead': dead_sprites[0:1],
        }
        self.anchor = (7, 16)
        self.dead_anchor = (13, 12)

# It is convenient to create an instance of the player in each level, rather than "moving" the player between levels:
class Player(BaseEntity):
    # keeping track of where we are facing even if we aren't moving
    FACING_R = 10
    FACING_L = 11
    FACING_U = 12
    FACING_D = 13

    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos)

        self.current_anim = 'right'
        self.swim_anim = 'swim_right'
        self.dead_anim = 'dead'
        self.anim_phase = 0
        self.stamina = MAX_STAMINA
        self.desired_velo = Vec2(0,0)
        self.in_water = False
        self.dead = False
        self.death_counter = 0
        self.time_until_next_step = 0
        self.last_step_sound = None
        self.facing = self.FACING_R

    def get_render_info(self):
        anim = assets.anims[self.current_anim]
        swim_anim = assets.swim_anims[self.swim_anim]
        dead_anim = assets.dead_anims[self.dead_anim]
        frame = int(self.anim_phase * len(anim)) % len(anim)
        swim_frame = int(self.anim_phase * len(swim_anim)) % len(swim_anim)
        dead_frame = int(self.anim_phase * len(dead_anim)) % len(dead_anim)
        return {
            'sprite': anim[frame] if self.in_water == False and self.dead == False else (dead_anim[dead_frame]) if self.dead else(swim_anim[swim_frame]),
            'pos': self.body.position,
            'anchor': assets.dead_anchor if self.dead else assets.anchor,
        }

    def handle_input(self, keys, events, dt):
        if self.dead == False:
            # determine desired player velocity based on keyboard input
            self.desired_velo = Vec2()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.desired_velo += Vec2(-1, 0)
                self.current_anim = 'left'
                self.swim_anim = 'swim_left'
                self.facing = self.FACING_L
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.desired_velo += Vec2(1, 0)
                self.current_anim = 'right'
                self.swim_anim = 'swim_right'
                self.facing = self.FACING_R
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.desired_velo += Vec2(0, -1)
                self.facing = self.FACING_U
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.desired_velo += Vec2(0, 1)
                self.facing = self.FACING_D

        # normalize and scale desired velocity
        if not self.desired_velo.is_zero():
            multiplier = PLAYER_SPEED
            if keys[pygame.K_SPACE]:
                if self.stamina >= 30:
                    multiplier += PLAYER_SPEED_BOOST
                    self.stamina = self.stamina - 10
            else:
                self.stamina = self.stamina + 1
                if self.stamina > MAX_STAMINA:
                    self.stamina = MAX_STAMINA
            self.desired_velo = self.desired_velo.normalized() * multiplier

        # apply force to player body to make its velocity approach the desired velocity
        velo_mult = 1
        tile_props = self.get_current_tile_props()
        if tile_props and tile_props.get('water'):
            self.in_water = True
            velo_mult = 0.5
        else:
            self.in_water = False
        self.apply_force_to_achieve_velocity(self.desired_velo*velo_mult, PLAYER_MOVEMENT_STRENGTH)

        # # update player sprite frame
        if self.desired_velo.is_zero():
            self.anim_phase = 0
            self.time_until_next_step = 0
        else:
            PLAYER_WALKING_ANIM_TIME = 0.2
            self.anim_phase += dt / PLAYER_WALKING_ANIM_TIME

            self.time_until_next_step -= dt
            if self.time_until_next_step <= 0:
                self.time_until_next_step += 0.3 + 0.1*random.random()
                if self.in_water:
                    choices = ['fsw1', 'fsw2', 'fsw3']
                else:
                    choices = ['fs1', 'fs2', 'fs3', 'fs4']

                if self.last_step_sound in choices:
                    choices.remove(self.last_step_sound)
                sfx = random.choice(choices)
                self.last_step_sound = sfx
                get_audio().play_sfx(sfx)

    def is_player(self):
        return True

    def kill(self):
        if not self.dead:
            self.dead = True
            get_audio().play_sfx('death')

    def die_if_tile_kills_you(self):
        tile_props = self.get_current_tile_props()
        if tile_props and tile_props.get('kills you'):
            self.kill()

    def act(self, dt):
        if self.in_water and not self.desired_velo.is_zero():
            for i in range(10):
                particle = WaterParticle(self.level, self.body.position, (random.uniform(-50, 50), random.uniform(-100, -50)))
                self.level.entities.append(particle)
        
        self.die_if_tile_kills_you()
        if self.dead:
            self.desired_velo = Vec2(0,0)
            self.death_counter += 1
            if self.death_counter >= 60:
                self.remove()

    def get_lighting(self):
        return 70
    
    def get_lighting_offset(self):
        light_delta = 30
        light_dir = None
        if self.desired_velo.is_zero():
            if self.facing == self.FACING_R:
                return (light_delta, 0)
            elif self.facing == self.FACING_L:
                return (-light_delta, 0)
            elif self.facing == self.FACING_U:
                return (0, -light_delta)
            else:
                return (light_delta, 0)
        else:
            light_dir = self.desired_velo.normalized()
            light_dir *= light_delta     # how far away the bright spot of our headlamp is
            return light_dir

    def remove(self):
        super().remove()
        player_state.total_lives -= 1

