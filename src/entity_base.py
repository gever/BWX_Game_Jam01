from vec2 import Vec2

class BaseEntity:
    def __init__(self):
        pass

    def apply_force_to_achieve_velocity(self, desired_velo, max_accel):
        velocity_diff = desired_velo - Vec2(self.body.velocity[0], self.body.velocity[1])
        movement_force = velocity_diff * (max_accel * self.body.mass)
        self.body.apply_force_at_local_point((movement_force.x, movement_force.y))

    def move_towards(self, target_pos, max_speed, max_accel):
        pos_diff = target_pos - self.body.position
        if pos_diff.length > 0:
            desired_velocity = pos_diff.normalized() * max_speed
        else:
            desired_velocity = pymunk.Vec2d(0, 0)
        self.apply_force_to_achieve_velocity(desired_velocity, max_accel)

    def handle_input(self, keys, events, dt):
        # safe to ignore by default
        pass

    def get_render_info(self):
        # not safe to ignore by default
        raise NotImplementedError
