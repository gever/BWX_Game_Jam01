import os
import pygame

SFX_MAP = {
    'rasp': 'rasp.wav',
}

class AudioEngine:
    def __init__(self):
        pygame.mixer.init()

        self.sfx = {}
        for key, fn in SFX_MAP.items():
            self.sfx[key] = pygame.mixer.Sound(os.path.join('../sfx', fn))

    def play_sfx(self, key):
        pygame.mixer.Sound.play(self.sfx[key])
