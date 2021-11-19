import pygame
from model import *

BLACK = [0, 0, 0]
pygame.init()

def game_start():
    global Player1, Player2
    Player1 = Player(1000, 400)
    Player2 = Player(200, 400)

def game_over():
   pass

def handler(event):
    return event.type


finished = False

FPS = 30
screen = pygame.display.set_mode((1200, 900))


clock = pygame.time.Clock()
game_start()
pygame.display.update()

while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type ==  pygame.KEYDOWN:
            #Обработка событий клавиатуры
            handler(event)

    #вызов обсчёта модели
    #tick()

    screen.fill(BLACK)

    pygame.display.update()

pygame.quit()