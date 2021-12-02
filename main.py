import pygame
import keyboard
from model import tick, Button, start
from view import *
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
        addacc_y -= 0.5 * 30 / FPS
    if keyboard.is_pressed('s'):
        addacc_y += 0.5 * 30 / FPS
    if keyboard.is_pressed('a'):
        addacc_x -= 0.5 * 30 / FPS
    if keyboard.is_pressed('d'):
        addacc_x += 0.5 * 30 / FPS
    return addacc_x, addacc_y


def init_operate_p2():
    addacc_x = 0
    addacc_y = 0
    if keyboard.is_pressed('up'):
        addacc_y -= 0.5
    if keyboard.is_pressed('down'):
        addacc_y += 0.5
    if keyboard.is_pressed('left'):
        addacc_x -= 0.5
    if keyboard.is_pressed('right'):
        addacc_x += 0.5
    return addacc_x, addacc_y


def controller():
    global finished, stop, play, pause, game_over
    if stop:
        button_load = Button(300, 'Load Game')
        button_play = Button(400, 'New Game')
        button_options = Button(500, 'Options')
        button_exit = Button(600, 'Exit')
        buttons = [button_load, button_play, button_options, button_exit]
        for button in buttons:
            image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = pygame.mouse.get_pos()
                if button_load.pressed(mouse_coords, button_load.coords1, button_load.coords3):
                    stop = False
                    play = True
                if button_play.pressed(mouse_coords, button_play.coords1, button_play.coords3):
                    stop = False
                    play = True
                    start()
                if button_exit.pressed(mouse_coords, button_exit.coords1, button_exit.coords3):
                    finished = True
                if button_options.pressed(mouse_coords, button_exit.coords1, button_exit.coords3):
                    pass
    if play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        if keyboard.is_pressed('Esc'):
            play = False
            pause = True

    if pause:
        button_return = Button(400, 'Main Menu')
        button_back = Button(500, 'Back')
        buttons = [button_return, button_back]
        for button in buttons:
            image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = pygame.mouse.get_pos()
                if button_return.pressed(mouse_coords, button_return.coords1, button_return.coords3):
                    pause = False
                    stop = True
                    screen.fill(BLACK)
                if button_back.pressed(mouse_coords, button_back.coords1, button_back.coords3):
                    pause = False
                    play = True
    if game_over:
        play = False
        button_end = Button(675, 'Main Menu')
        buttons = [button_end]
        for button in buttons:
            image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text)
        pygame.display.update()
        over_surf = pygame.font.Font(None, 150)
        over_text = over_surf.render('Game Over', True, RED)
        screen.blit(over_text, (250, 400))
        result_surf = pygame.font.Font(None, 125)
        result_text = result_surf.render('Someone has won!', True, BLUE)
        screen.blit(result_text, (175, 550))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = pygame.mouse.get_pos()
                if button_end.pressed(mouse_coords, button_end.coords1, button_end.coords3):
                    game_over = False
                    stop = True
                    screen.fill(BLACK)
        start()

finished = play = pause = game_over = False
stop = True

FPS = 30
dt = 0
screen = pygame.display.set_mode((1024, 1024))

clock = pygame.time.Clock()
pygame.display.update()
field_drawer = Drawer(screen)
start()

while not finished:
    clock.tick(FPS)
    controller()

    if play:
        p1x, p1y = init_operate_p1()
        p2x, p2y = init_operate_p2()
        controls = [p1x, p1y, p2x, p2y]
        Player1, Player2, spike, field, dt = tick(dt, controls)
        field_drawer.update(field, dt)
        display_player(screen, Player1)
        display_player(screen, Player2)
        pygame.draw.polygon(screen, [255, 255, 255], [[spike.x2, spike.y2], [spike.x3, spike.y3], [spike.x1, spike.y1]])
        pygame.display.update()
        if not Player1.live or not Player2.live:
            game_over = True

pygame.quit()
