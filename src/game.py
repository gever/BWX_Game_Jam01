import pygame
from vec2 import Vec2
from map import TiledMap
from audio import AudioEngine

TILE_SIZE = 16
PLAYER_SPEED = 1.5

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 576)) # this should probably be 16:9
clock = pygame.time.Clock()
audio = AudioEngine()
running = True

current_map = TiledMap('../maps/dungeon_map.tmx')

base_tile_layer_idx = current_map.get_first_tile_layer_index()

CHARACTER_SIZE = 16
CHARACTER_ANCHOR = Vec2(8, 14)
character_sheet = pygame.image.load('../gfx/Sprout Lands - Sprites - premium pack/Characters/Basic Charakter Spritesheet.png').convert_alpha()
character_down_frames = []
for i in range(0, 4):
    frame = character_sheet.subsurface((16*(3*i + 1), 16, 16, 16))
    character_down_frames.append(frame)
character_frame_num = 0

spawn_point = current_map.get_object_by_name('player_spawn')
player_pos = Vec2(spawn_point.x, spawn_point.y)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check keyboard input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    # determine player movement
    player_dir = Vec2()
    if keys[pygame.K_LEFT]:
        player_dir += Vec2(-1, 0)
    if keys[pygame.K_RIGHT]:
        player_dir += Vec2(1, 0)
    if keys[pygame.K_UP]:
        player_dir += Vec2(0, -1)
    if keys[pygame.K_DOWN]:
        player_dir += Vec2(0, 1)

    if player_dir.is_zero():
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

        player_v = player_dir.normalized() * PLAYER_SPEED

        prev_player_tile_coords = player_pos / TILE_SIZE
        prev_tile_props = current_map.get_tile_props_by_coords(base_tile_layer_idx, prev_player_tile_coords.x, prev_player_tile_coords.y)

        new_player_pos = player_pos + player_v
        new_player_tile_coords = new_player_pos / TILE_SIZE
        new_tile_props = current_map.get_tile_props_by_coords(base_tile_layer_idx, new_player_tile_coords.x, new_player_tile_coords.y)
        passable = new_tile_props.get('passable', False)
        if passable:
            player_pos = new_player_pos

            if prev_tile_props['id'] != new_tile_props['id']:
                if new_tile_props['id'] == 65: # hardcoded special tile id
                    audio.play_sfx('rasp')

    # render map to a temporary surface
    temp_surface = current_map.render_map_to_new_surface()

    # draw player placeholder
    #pygame.draw.circle(temp_surface, (255, 0, 0), (player_pos.x, player_pos.y), 3)

    # render character sprite
    char_render_frame = character_down_frames[character_frame_num]
    char_render_pos = player_pos - CHARACTER_ANCHOR
    temp_surface.blit(char_render_frame, (char_render_pos.x, char_render_pos.y))

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
