import os
import pygame

audio_engine = None

SFX_MAP = {
    'mine_rock': 'miningNoises.wav',
    'death': 'death.wav',
    'fs1': 'footstep_1.wav',
    'fs2': 'footstep_2.wav',
    'fs3': 'footstep_3.wav',
    'fs4': 'footstep_4.wav',
    'fsw1': 'footstep_water_1.wav',
    'fsw2': 'footstep_water_2.wav',
    'fsw3': 'footstep_water_3.wav',
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

        self.sfx = {}
        for key, fn in SFX_MAP.items():
            self.sfx[key] = pygame.mixer.Sound(os.path.join('../sfx', fn))

        self.music_idx = 0

    def play_sfx(self, key, loop=False):
        #pygame.mixer.Sound.play(self.sfx[key])
        self.sfx[key].play(-1 if loop else 0)

    def _play_music_by_idx(self, idx):
        music_path = os.path.join('../music', MUSIC_PLAYLIST[idx])
        print('Playing music:', music_path)
        pygame.mixer.music.load(os.path.join('../music', music_path))
        pygame.mixer.music.play(0)

    def start_music(self):
        self._play_music_by_idx(self.music_idx)

    def update_music(self):
        if not pygame.mixer.music.get_busy():
            self.music_idx = (self.music_idx + 1) % len(MUSIC_PLAYLIST)
            self._play_music_by_idx(self.music_idx)

def init_audio():
    global audio_engine
    audio_engine = AudioEngine()

def get_audio():
    return audio_engine
