import os
import pygame

audio_engine = None

SFX_MAP = {
    'lava_death': 'better sizzle.wav',
    'mine_rock': 'miningNoises.wav',
    'death': 'death.wav',
    'fs1': 'footstep_1.wav',
    'fs2': 'footstep_2.wav',
    'fs3': 'footstep_3.wav',
    'fs4': 'footstep_4.wav',
    'fsw1': 'footstep_water_1.wav',
    'fsw2': 'footstep_water_2.wav',
    'fsw3': 'footstep_water_3.wav',
    'eating': 'eating a shroom.wav',
    'doubler': 'stock_doubler_sfx.mp3',
    'falling': 'falling.wav',
    'pick_hit': '1 pick hit.wav'
}

MUSIC_PLAYLIST = [
    'eerie.mp3',
    'caveBarBlues.wav',
    'backround music 1.wav',
    'chillCaveMusicRemaster.wav',
]

class AudioEngine:
    def __init__(self):
        pygame.mixer.init()

        self.no_music = True
        self.sfx = {}
        for key, fn in SFX_MAP.items():
            self.sfx[key] = pygame.mixer.Sound(os.path.join('../sfx', fn))

        self.music_idx = 0

    def play_sfx(self, key, loop=False):
        self.sfx[key].play(-1 if loop else 0)

    def _play_music_by_idx(self, idx):
        if not self.no_music:
            music_path = os.path.join('../music', MUSIC_PLAYLIST[idx])
            print('Playing music:', music_path)
            pygame.mixer.music.load(os.path.join('../music', music_path))
            pygame.mixer.music.play(0)

    def start_music(self):
        if not self.no_music:
            self._play_music_by_idx(self.music_idx)
    def stop_music(self):
        pygame.mixer.music.stop()
        self.no_music = True

    def update_music(self):
        if not pygame.mixer.music.get_busy():
            self.music_idx = (self.music_idx + 1) % len(MUSIC_PLAYLIST)
            self._play_music_by_idx(self.music_idx)

def init_audio():
    global audio_engine
    audio_engine = AudioEngine()

def get_audio():
    return audio_engine
