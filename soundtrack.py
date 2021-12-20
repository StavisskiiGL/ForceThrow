import pygame

class Volume_control():
    def __init__(self):
        self.music = 'play'
        self.activate_sound = False
        self.music_volume = 0.5
        self.sounds_volume = 0.5
        self.activ_sound = pygame.mixer.Sound('activatesound.wav')

    def music_control(self, manager):
        """Управляет переключением музыки в зависимости от нахождения в меню или игре"""

        if manager.stop:
            if self.music != 'menu':
                pygame.mixer.music.fadeout(500)
                self.music = 'menu'
                pygame.mixer.music.unload()
                pygame.mixer.music.load('menumusic.mp3')
                pygame.mixer.music.play()

        if manager.play and manager.not_started:
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.rewind()
            pygame.mixer.music.play()

        if manager.play:
            if self.music != 'play':
                pygame.mixer.music.fadeout(500)
                self.music = 'play'
                pygame.mixer.music.unload()
                pygame.mixer.music.load('gamemusic.mp3')
                pygame.mixer.music.play()
        if manager.options:
            pygame.mixer.music.set_volume(self.music_volume)

    def sounds_control(self, manager):
        if self.activate_sound:
            pygame.mixer.Sound.play(self.activ_sound)
            self.activate_sound = False
        if manager.options:
            pygame.mixer.Sound.set_volume(self.activ_sound, self.sounds_volume)
