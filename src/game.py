import time
import pygame
from vec2 import Vec2
from map import TiledMap
from audio import AudioEngine
import pymunk

TILE_SIZE = 16
PLAYER_SPEED = 100
PLAYER_MOVEMENT_MAX_ACCEL = 25

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 576)) # this should probably be 16:9
clock = pygame.time.Clock()
audio = AudioEngine()
font = pygame.font.Font(None, 16)
running = True
show_fps = True

current_map = TiledMap('../maps/dungeon_map.tmx')

base_tile_layer_idx = current_map.get_first_tile_layer_index()

CHARACTER_SIZE = 16
CHARACTER_ANCHOR = Vec2(7, 12)
character_sheet = pygame.image.load('../gfx/Sprout Lands - Sprites - premium pack/Characters/Basic Charakter Spritesheet.png').convert_alpha()
character_down_frames = []
for i in range(0, 4):
    frame = character_sheet.subsurface((16*(3*i + 1), 16, 16, 16))
    character_down_frames.append(frame)
character_frame_num = 0

spawn_point = current_map.get_object_by_name('player_spawn')

# physics setup
space = pymunk.Space()

# create player body and collision shape
player_body = pymunk.Body(1, float('inf'))
player_body.position = (spawn_point.x, spawn_point.y)
player_shape = pymunk.Circle(player_body, 6)
player_shape.elasticity = 0
space.add(player_body, player_shape)

# create a collision square for each impassable tile
impassable_tile_coords = current_map.list_impassable_tile_coords()
for (x, y) in impassable_tile_coords:
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (x*TILE_SIZE + TILE_SIZE/2, y*TILE_SIZE + TILE_SIZE/2)
    shape = pymunk.Poly.create_box(body, (TILE_SIZE, TILE_SIZE), 0.1)
    shape.elasticity = 0
    space.add(body, shape)

# start background music
audio.play_sfx('water_drops', loop=True)

last_time = time.time()

while running:
    # calculate time since last frame
    dt = time.time() - last_time
    last_time = time.time()

    # advance physics simulation
    space.step(dt)

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                show_fps = not show_fps

    # check keyboard input (currently pressed keys)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    # determine desired player velocity based on keyboard input
    player_desired_velo = Vec2()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_desired_velo += Vec2(-1, 0)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_desired_velo += Vec2(1, 0)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_desired_velo += Vec2(0, -1)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_desired_velo += Vec2(0, 1)

    # normalize and scale desired velocity
    if not player_desired_velo.is_zero():
        player_desired_velo = player_desired_velo.normalized() * PLAYER_SPEED

    # apply force to player body to make its velocity approach the desired velocity
    velocity_diff = player_desired_velo - Vec2(player_body.velocity[0], player_body.velocity[1])
    if dt > 0:
        movement_force = velocity_diff * (PLAYER_MOVEMENT_MAX_ACCEL * player_body.mass)
    else:
        movement_force = Vec2()
    player_body.apply_force_at_local_point((movement_force.x, movement_force.y))

    # update character sprite frame
    if player_desired_velo.is_zero():
        character_frame_num = 0
    else:
        if character_frame_num == 0:
            character_frame_num = 2
        elif character_frame_num == 2:
            character_frame_num = 3
        elif character_frame_num == 3:
            character_frame_num = 2
        else:
            assert False

    # render map to a temporary surface
    temp_surface = current_map.render_map_to_new_surface()

    # render character sprite
    char_render_frame = character_down_frames[character_frame_num]
    char_render_pos = player_body.position - CHARACTER_ANCHOR
    temp_surface.blit(char_render_frame, (char_render_pos.x, char_render_pos.y))

    # render FPS
    if show_fps:
        rounded_fps = str(round(clock.get_fps(), 2))
        fps_text = font.render(rounded_fps, True, (255, 255, 255))
        temp_surface.blit(fps_text, (temp_surface.get_width() - fps_text.get_width(), 0))

    # determine factor by which we need to scale map surface to fit display
    scale = min(screen.get_width() / temp_surface.get_width(), screen.get_height() / temp_surface.get_height())
    x_offset = (screen.get_width() - temp_surface.get_width() * scale) / 2
    y_offset = (screen.get_height() - temp_surface.get_height() * scale) / 2

    # now resize the temporary surface to the size of the display
    # this will also 'blit' the temp surface to the display
    scaled_temp_surface = pygame.transform.scale_by(temp_surface, scale)

    # copy the scaled temp surface to the display (centered)
    screen.blit(scaled_temp_surface, (x_offset, y_offset))

    # "flip" the display to update what the user sees
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
