import pygame

light_texture = None

def load_light_texture():
    global light_texture
    light_texture = pygame.image.load('../gfx/light.png').convert_alpha()

# each light has keys 'x', 'y', 'r'
def create_light_surface(width, height, lights):
    surface = pygame.Surface((width, height))
    surface.fill((0, 0, 0))

    for light in lights:
        light_surface = pygame.transform.scale(light_texture, (light['r']*2, light['r']*2))
        surface.blit(light_surface, (light['x'] - light['r'], light['y'] - light['r']))

    return surface
