import pygame

from entity_base import BaseEntity
from entity_waterblob import WaterBlob
from entity_rock import Rock

def load():
    global assets
    assets = LavaBlobAssets()

class LavaBlobAssets:
    def __init__(self):
        spritesheet = pygame.image.load('../gfx/Lava Blob.png').convert_alpha()
        paused_spritesheet = pygame.image.load('../gfx/Half Stone Lava Blob.png').convert_alpha()
        stone_spritesheet = pygame.image.load('../gfx/Stone Lava Blob.png').convert_alpha()
        blank_spritesheet = pygame.image.load('../gfx/in_lava_lava_blob.png').convert_alpha()
        self.stonesprite = stone_spritesheet.subsurface((0, 0, 16, 12))
        self.spritelist = []
        self.pausedspritelist = []
        self.inlavaspritelist = []
        for i in range (0,4):
            main_frame = spritesheet.subsurface(((20*i), 0, 16, 12))
            self.spritelist.append(main_frame)
        for i in range (0,4):
            paused_frame = paused_spritesheet.subsurface(((20*i), 0, 16, 12))
            self.pausedspritelist.append(paused_frame)
        for i in range (0,4):
            #sleep()
            in_lava_frame = blank_spritesheet.subsurface(((17*i), 0, 16, 12))
            self.inlavaspritelist.append(in_lava_frame)
        self.anchor = (8, 14)

class LavaBlob(BaseEntity):
    def __init__(self, level, initial_pos):
        super().__init__(level, initial_pos, square=True)
        self.chasing = False
        self.time_until_death = 1.5
        self.paused = False
        self.less_speed = 0
        self.timer = 0
        self.time_unil_stone = 2.5
        self.stone = False
        self.inlava = False
        self.exit_lava = 0

    def get_render_info(self):
        self.main_frame = int(self.timer) % len(assets.spritelist)
        self.paused_frame = int(self.timer) % len(assets.pausedspritelist)
        self.in_lava_frame = int(self.timer) % len(assets.inlavaspritelist)
        return {
            'sprite': assets.inlavaspritelist[self.in_lava_frame] if self.inlava else (assets.stonesprite if self.stone else (assets.pausedspritelist[self.paused_frame] if self.paused else assets.spritelist[self.main_frame])),
            'pos': self.body.position,
            'anchor': assets.anchor,
        }

    def get_lighting(self):
        return None if self.stone else (50 if self.paused else 100)

    def handle_entity_collision(self, other_entity):
        if (not self.paused or not self.stone) and not self.paused and not self.stone:
            # TODO: trigger player death noise
            if other_entity.is_player():
                other_entity.remove()
                return

            # TODO: trigger water blob death noise
            if isinstance(other_entity, WaterBlob):
                other_entity.remove()

            if isinstance(other_entity, Rock):
                other_entity.remove()
                self.remove()

    def act(self,dt):
        self.timer += dt*5
        MAX_SPEED = 85
        MOVEMENT_STRENGTH = 15
        player = self.get_nearest_player()

        tile_props = self.get_current_tile_props()
        if tile_props and tile_props.get('water'):
            self.paused = True

        tile_props = self.get_current_tile_props()
        if tile_props and tile_props.get('kills you'):
            self.paused = False
        #    self.inlava = True
            self.time_until_death = 2.5
            self.time_unil_stone = 2.5
        #else:
            #if self.in_lava_frame == 0 or self.in_lava_frame == 4:
        #    self.inlava = False

        if player:
            dist = player.body.position.get_distance(self.body.position)
            if dist < 80:
               self.chasing = True
            if dist > 80 and (tile_props and tile_props.get('kills you')):
                self.inlava = True
            else:
                self.exit_lava += 1
                if self.exit_lava > 2:
                    self.inlava = False
                    self.exit_lava = 0

            if self.stone:
                self.chasing = False
                MAX_SPEED = 0
                MOVEMENT_STRENGTH = 0


            if self.paused == True:
               # self.chasing = False
                self.time_unil_stone -= dt
                if self.time_unil_stone < 0:
                    self.stone = True
                MAX_SPEED = 30
                MOVEMENT_STRENGTH = 90

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
