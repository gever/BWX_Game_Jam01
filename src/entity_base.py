from vec2 import Vec2
import pymunk

class BaseEntity:
    def __init__(self, level, initial_pos):
        self.level = level
        self.initial_pos = initial_pos

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

    def move_towards_player(self, max_speed, strength):
        # find closest player (in case there are multiple players)
        player = None
        closest_dist = float('inf')
        for entity in self.level.entities:
            if entity.is_player():
                dist = (entity.body.position - self.body.position).length
                if dist < closest_dist:
                    player = entity
                    closest_dist = dist

        if player:
            pos_diff = player.body.position - self.body.position
            if pos_diff.length > 0:
                desired_velocity = pos_diff.normalized() * max_speed
            else:
                desired_velocity = pymunk.Vec2d(0, 0)
            self.apply_force_to_achieve_velocity(desired_velocity, strength)

    def handle_input(self, keys, events, dt):
        # safe to ignore by default
        pass

    def act(self):
        # safe to ignore by default
        pass

    def get_render_info(self):
        # not safe to ignore by default
        raise NotImplementedError

    def reset(self):
        self.body.position = pymunk.Vec2d(self.initial_pos[0], self.initial_pos[1])
        self.body.velocity = (0, 0)

    def is_player(self):
        return False
