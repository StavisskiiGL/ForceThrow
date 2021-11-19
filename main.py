import pygame
from model import *

Player1 = 0
Player2 = 0
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
pygame.init()


def game_over():
   pass


def handler(event):
    return event.type


finished = False

FPS = 10
screen = pygame.display.set_mode((1024, 1024))


clock = pygame.time.Clock()
pygame.display.update()

while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            #Обработка событий клавиатуры
            handler(event)

    #вызов обсчёта модели
    screen.fill(BLACK)
    Player1, Player2 = tick()
    pygame.draw.circle(screen, RED, [Player1.x, 1024 - Player1.y], Player1.size)
    pygame.draw.circle(screen, BLUE, [Player2.x, 1024 - Player2.y], Player2.size)
    print(Player1.x, Player1.y)
    pygame.display.update()

pygame.quit()