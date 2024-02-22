import time

import pygame

from audio import init_audio, get_audio
from config import *
from levels_loader import load_levels
from entities_loader import load_entities
from level_base import BaseLevel

# pygame setup
pygame.init()

screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

# screen = pygame.display.set_mode((screen_width, screen_height)) # this should probably be 16:9
screen = pygame.display.set_mode((960, 540)) # this should probably be 16:9
clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)
running = True
show_fps = True
init_audio()

# start background music
get_audio().play_sfx('water_drops', loop=True)

# load all entities and levels
entities = load_entities()
levels = load_levels()

current_level_idx = 0
current_level = levels[current_level_idx]
current_level.start()

def switch_level(new_level_idx):
    global current_level, current_level_idx
    current_level.stop()
    current_level = levels[new_level_idx]
    current_level.start()
    current_level_idx = new_level_idx

last_time = time.time()
while running:
    # calculate time since last frame
    dt = time.time() - last_time
    last_time = time.time()

    # poll for events
    unhandled_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                show_fps = not show_fps
            elif event.key == pygame.K_r:
                current_level.base_reset()
                current_level.level_reset()
            elif event.key == pygame.K_LEFTBRACKET:
                switch_level((current_level_idx - 1) % len(levels))
            elif event.key == pygame.K_RIGHTBRACKET:
                switch_level((current_level_idx + 1) % len(levels))
            else:
                unhandled_events.append(event)
        else:
            unhandled_events.append(event)

    # check keyboard input (currently pressed keys)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    # do core work based on the current level
    current_level.handle_input(keys, unhandled_events, dt)
    current_level.advance_simulation(dt)
    if current_level.level_complete():
        switch_level((current_level_idx + 1) % len(levels))

    render_surface = current_level.render()

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

    # copy the scaled temp surface to the display (centered)
    screen.blit(scaled_render_surface, (x_offset, y_offset))

    # "flip" the display to update what the user sees
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
