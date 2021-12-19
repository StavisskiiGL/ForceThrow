import pygame


def music_control(manager):
    """Управляет переключением музыки в зависимости от нахождения в меню или игре"""

    if manager.stop:
        if manager.music != 'menu':
            pygame.mixer.music.fadeout(500)
            manager.music = 'menu'
            pygame.mixer.music.unload()
            pygame.mixer.music.load('menumusic.mp3')
            pygame.mixer.music.play()

    if manager.play and manager.not_started:
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()

    if manager.play:
        if manager.music != 'play':
            pygame.mixer.music.fadeout(500)
            manager.music = 'play'
            pygame.mixer.music.unload()
            pygame.mixer.music.load('gamemusic.mp3')
            pygame.mixer.music.play()
    if manager.options:
        pygame.mixer.music.set_volume(manager.music_volume)


def sounds_control(manager):
    if manager.activate_sound:
        pygame.mixer.Sound.play(manager.activ_sound)
        manager.activate_sound = False
    if manager.options:
        pygame.mixer.Sound.set_volume(manager.activ_sound, manager.sounds_volume)
