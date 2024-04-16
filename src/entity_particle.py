import time

from entity_base import BaseEntity

from collision_types import COLLISION_TYPE_PARTICLE

class ParticleEntity(BaseEntity):
    def __init__(self, level, initial_pos, initial_velo):
        super().__init__(level, initial_pos, radius=1, collision_type=COLLISION_TYPE_PARTICLE, sensor=True)
        self.body.velocity = initial_velo
        self.creation_time = time.time()

    def act(self, dt):
        g = 300
        self.body.apply_force_at_local_point((0, g*self.body.mass))
        if time.time() - self.creation_time > .25:
            self.remove()
