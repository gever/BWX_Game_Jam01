import pygame
import pymunk

from level_base import BaseLevel
from collision_types import COLLISION_TYPE_IMPASSABLE_TILE

class Level(BaseLevel):
    def __init__(self, map_fn):
        super().__init__(map_fn)

        self.overlay_image = pygame.image.load('../gfx/starting_screen.png').convert_alpha()

    def reset_extra(self):
        ledge_body = pymunk.Body(1, float('inf'), body_type=pymunk.Body.STATIC)
        ledge_body.position = (0, 0)
        ledge_shape = pymunk.Poly(ledge_body, [(0, 35), (70, 35), (70, 50), (0, 50)])
        ledge_shape.collision_type = COLLISION_TYPE_IMPASSABLE_TILE
        ledge_shape.elasticity = 0
        self.space.add(ledge_body, ledge_shape)

        ledge_body = pymunk.Body(1, float('inf'), body_type=pymunk.Body.STATIC)
        ledge_body.position = (0, 0)
        ledge_shape = pymunk.Poly(ledge_body, [(0, 0), (0, 100), (-10, 100), (-10, 0)])
        ledge_shape.collision_type = COLLISION_TYPE_IMPASSABLE_TILE
        ledge_shape.elasticity = 0
        self.space.add(ledge_body, ledge_shape)

    def is_start_level(self):
        return True

    def level_complete(self):
        for entity in self.entities:
            if entity.is_player():
                if entity.body.position.y > 200:
                    return True

    def extra_advance_simulation(self, dt):
        for entity in self.entities:
            if entity.is_player():
                entity.body.apply_force_at_local_point((0, entity.body.mass*400))

    def render(self, apply_lighting):
        # render map to a temporary surface
        surface = self.map.render_map_to_new_surface()

        surface.blit(self.overlay_image, (0, 0))

        self.render_entities(surface)

        return surface
