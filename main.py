import pygame
import keyboard
from model import *

Player1 = 0
Player2 = 0
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
pygame.init()


def init_operate_p1():
    addacc_x = 0
    addacc_y = 0
    if keyboard.is_pressed('w'):
        addacc_y += 0.5
    if keyboard.is_pressed('s'):
        addacc_y -= 0.5
    if keyboard.is_pressed('a'):
        addacc_x -= 0.5
    if keyboard.is_pressed('d'):
        addacc_x += 0.5
    return addacc_x, addacc_y


def init_operate_p2():
    addacc_x = 0
    addacc_y = 0
    if keyboard.is_pressed('up'):
        addacc_y += 0.5
    if keyboard.is_pressed('down'):
        addacc_y -= 0.5
    if keyboard.is_pressed('left'):
        addacc_x -= 0.5
    if keyboard.is_pressed('right'):
        addacc_x += 0.5
    return addacc_x, addacc_y


def game_over():
   pass


finished = False

FPS = 30
dt = 0
screen = pygame.display.set_mode((1024, 1024))


clock = pygame.time.Clock()
pygame.display.update()

while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    #вызов обсчёта модели
    screen.fill(BLACK)
    p1x, p1y = init_operate_p1()
    p2x, p2y = init_operate_p2()
    controls = [p1x, p1y, p2x, p2y]
    Player1, Player2, dt = tick(dt, controls)
    pygame.draw.circle(screen, RED, [Player1.x, 1024 - Player1.y], Player1.size)
    pygame.draw.circle(screen, BLUE, [Player2.x, 1024 - Player2.y], Player2.size)
    pygame.display.update()

pygame.quit()