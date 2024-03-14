from vec2 import Vec2
import pymunk

from config import *
from collision_types import *

class BaseEntity:
    def __init__(self, level, initial_pos, *, radius=6, square = False, mass=1, static=False):
        self.level = level
        self.initial_pos = initial_pos

        self.body = pymunk.Body(mass, float('inf'), body_type=pymunk.Body.STATIC if static else pymunk.Body.DYNAMIC)
        self.body.position = self.initial_pos
        self.body.entity = self
        self.shape = pymunk.Poly(self.body, [(-radius,-radius),(radius,-radius),(radius,radius),(-radius,radius)]) if square else pymunk.Circle(self.body, radius)
        self.shape.collision_type = COLLISION_TYPE_ENTITY
        self.shape.elasticity = 0
        self.level.space.add(self.body, self.shape)

    def apply_force_to_achieve_velocity(self, desired_velo, strength):
        velocity_diff = desired_velo - Vec2(self.body.velocity[0], self.body.velocity[1])
        movement_force = velocity_diff * strength
        self.body.apply_force_at_local_point((movement_force.x, movement_force.y))

    def move_towards(self, target_pos, max_speed, strength):
        pos_diff = target_pos - self.body.position
        if pos_diff.length > 0:
            desired_velocity = pos_diff.normalized() * max_speed
        else:
            desired_velocity = pymunk.Vec2d(0, 0)
        self.apply_force_to_achieve_velocity(desired_velocity, strength)

    # find closest player (in case there are multiple players)
    def get_nearest_player(self):
        player = None
        closest_dist = float('inf')
        for entity in self.level.entities:
            if entity.is_player():
                dist = (entity.body.position - self.body.position).length
                if dist < closest_dist:
                    player = entity
                    closest_dist = dist
        return player

    def move_towards_player(self, max_speed, strength):
        player = self.get_nearest_player()

        if player:
            self.move_towards(player.body.position, max_speed, strength)

    def get_current_tile_props(self):
        return self.level._get_tile_props_by_coords(int(self.body.position.x/TILE_SIZE), int(self.body.position.y/TILE_SIZE))

    def die_if_tile_kills_you(self):
        tile_props = self.get_current_tile_props()
        if tile_props and tile_props.get('kills you'):
            self.remove()

    def remove(self):
        self.level.space.remove(self.body, self.shape)
        self.level.remove_entity(self)

    def handle_input(self, keys, events, dt):
        # safe to ignore by default
        pass

    def act(self, dt):
        # safe to ignore by default
        pass

    def handle_entity_collision(self, other_entity):
        # safe to ignore by default
        pass

    def handle_tile_collision(self):
        # safe to ignore by default
        pass

    def get_render_info(self):
        # not safe to ignore by default
        raise NotImplementedError

    # return radius number or None
    def get_lighting(self):
        # safe to ignore by default
        return None

    def is_player(self):
        return False
