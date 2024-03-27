import time
import math

import pygame

from audio import init_audio, get_audio
from config import *
from levels_loader import load_levels
from entities_loader import load_entities
from level_base import BaseLevel
from lighting import load_light_texture
from player_state import player_state

# pygame setup
pygame.init()

screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

# screen = pygame.display.set_mode((screen_width, screen_height)) # this should probably be 16:9
screen = pygame.display.set_mode((screen_width, screen_height)) # this should probably be 16:9
clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)
running = True
set_values = True
show_fps = False
apply_lighting = True
init_audio()

# start background music
get_audio().start_music()

# load all entities and levels
load_light_texture()
entities = load_entities()
levels = load_levels()

current_level_idx = 0
current_level = levels[current_level_idx]
current_level.reset()
current_level.start()

def switch_level(new_level_idx):
    global current_level, current_level_idx
    current_level.stop()
    current_level = levels[new_level_idx]
    print("current level:", current_level.map_fn)
    current_level.reset()
    current_level.start()
    current_level_idx = new_level_idx

last_time = time.time()
while running:
    # calculate time since last frame
    dt = time.time() - last_time
    last_time = time.time()

    get_audio().update_music()

    if set_values:
        konami = False
        check_1 = False
        check_2 = False
        check_3 = False
        check_4 = False
        check_5 = False
        check_6 = False
        check_7 = False
        check_8 = False
        check_9 = False
        check_10 = False
        checks_done = False
        any_check = False
        set_values = False

    # poll for events
    unhandled_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
            running = False
        elif event.type == pygame.KEYDOWN:
            if check_1 or check_2 or check_3 or check_4 or check_5 or check_6 or check_7 or check_8 or check_9 or check_10 or checks_done:
                any_check = True
            else:
                any_check = False
            if event.key == pygame.K_f:
                show_fps = not show_fps
            if event.key == pygame.K_SPACE and check_10:
                konami = True
                checks_done = True
            elif event.key != pygame.K_SPACE and check_10:
                check_10 = False
            elif event.key == pygame.K_q and check_9:
                check_10 = True
                check_9 = False
            elif event.key != pygame.K_q and check_9:
                check_9 = False
            elif event.key == pygame.K_e and check_8:
                check_9 = True
                check_8 = False
            elif event.key != pygame.K_e and check_8:
                check_8 = False
            elif event.key == pygame.K_d and check_7:
                check_8 = True
                check_7 = False
            elif event.key != pygame.K_d and check_7:
                check_7 = False
            elif event.key == pygame.K_a and check_6:
                check_7 = True
                check_6 = False
            elif event.key != pygame.K_a and check_6:
                check_6 = False
            elif event.key == pygame.K_d and check_5:
                check_6 = True
                check_5 = False
            elif event.key != pygame.K_d and check_5:
                check_5 = False
            elif event.key == pygame.K_a and check_4:
                check_5 = True
                check_4 = True
            elif event.key != pygame.K_a and check_4:
                check_4 = False
            elif event.key == pygame.K_s and check_3:
                check_4 = True
                check_3 = False
            elif event.key != pygame.K_s and check_3:
                check_3 = False
            elif event.key == pygame.K_s and check_2:
                check_3 = True
                check_2 = False
            elif event.key != pygame.K_s and check_2:
                check_2 = False
            elif event.key == pygame.K_w and check_1:
                check_2 = True
                check_1 = False
            elif event.key != pygame.K_w and check_1:
                check_1 = False
            if event.key == pygame.K_w and any_check == False:
                check_1 = True
            elif event.key == pygame.K_r:
                player_state.total_lives -= 1
                current_level.reset()
            elif event.key == pygame.K_t:
                # demonstrate changing tile layer visibility
                tmx_data = current_level.map.set_layer_visibility('Tile Layer 2', False)
                current_level._create_tile_physics()
            elif event.key == pygame.K_l:
                apply_lighting = not apply_lighting
            elif event.key == pygame.K_MINUS:
                screen = pygame.display.set_mode((960, 540))
            elif event.key == pygame.K_PLUS:
                screen = pygame.display.set_mode((screen_width, screen_height))
            elif event.key == pygame.K_LEFTBRACKET:
                switch_level((current_level_idx - 1) % len(levels))
            elif event.key == pygame.K_RIGHTBRACKET:
                switch_level((current_level_idx + 1) % len(levels))
            else:
                unhandled_events.append(event)
        else:
            unhandled_events.append(event)
    if konami:
        player_state.total_lives = 1000

    # check keyboard input (currently pressed keys)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    # do core work based on the current level
    current_level.handle_input(keys, unhandled_events, dt)
    current_level.advance_simulation(dt)
    if current_level.level_complete():
        switch_level((current_level_idx + 1) % len(levels))

    render_surface = current_level.render(apply_lighting)

    if player_state.total_lives == 0:
        switch_level(0)
        player_state.restart()

    # render FPS
    if show_fps:
        rounded_fps = str(round(clock.get_fps(), 2))
        fps_text = font.render(rounded_fps, True, (255, 255, 255))
        render_surface.blit(fps_text, (render_surface.get_width() - fps_text.get_width(), 0))

    # determine factor by which we need to scale map surface to fit display
    scale = min(screen.get_width() / render_surface.get_width(), screen.get_height() / render_surface.get_height())
    x_offset = (screen.get_width() - render_surface.get_width() * scale) / 2
    y_offset = (screen.get_height() - render_surface.get_height() * scale) / 2

    # now resize the render surface to the size of the display
    # this will also 'blit' the temp surface to the display
    scaled_render_surface = pygame.transform.scale_by(render_surface, scale)

    seeing_double = current_level.get_seeing_double() and ENABLE_SEEING_DOUBLE

    if seeing_double:
        # darken scaled_render_surface
        scaled_render_surface.fill((128, 128, 128), special_flags=pygame.BLEND_RGB_MULT)

    # fill screen with black (otherwise "seeing double" effect leaves weird edges)
    screen.fill((0, 0, 0))

    # copy the scaled temp surface to the display (centered)
    screen.blit(scaled_render_surface, (x_offset, y_offset))

    if seeing_double:
        screen.blit(scaled_render_surface, (x_offset + math.cos(2*time.time()) * 8, y_offset + math.sin(2*time.time()) * 8), special_flags=pygame.BLEND_RGB_ADD)

    # "flip" the display to update what the user sees
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
