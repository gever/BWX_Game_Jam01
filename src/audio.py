import os
import pygame

audio_engine = None

SFX_MAP = {
    'rasp': 'rasp.wav',
    'water_drops': 'water-drops-daniel_simon.mp3',
}

MUSIC_PLAYLIST = [
    'backround music 1.wav',
    'backround music 2.wav',
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
