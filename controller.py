import pygame
import keyboard
from model import tick, Button, start, InputBox, screen, restart
from view import *

Player1 = 0
Player2 = 0
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
ORANGE = [200, 100, 0]

clock = pygame.time.Clock()
pygame.display.update()
field_drawer = Drawer(screen)

play = pause = game_over = finished = game_break = need_break = False
stop = not_started = True
dt = 0


def main_cycle():
    "Основной цикл: управление объектами во время игры"
    global game_over, dt, Player1, Player2, game_break, play
    clock.tick(FPS)
    p1x, p1y = init_operate_p1()
    p2x, p2y = init_operate_p2()
    controls = [p1x, p1y, p2x, p2y]
    Player1, Player2, spike, field, dt, objects = tick(dt, controls)
    field_drawer.update(field, dt)
    display_player(screen, Player1)
    display_player(screen, Player2)

    if type(objects[0]) != type(1):
        print(objects[0])
        if not objects[0].used:
            pygame.draw.polygon(screen, objects[0].color, objects[0].drawdata)
    pygame.draw.polygon(screen, [255, 255, 255],
                        [[spike.x2, spike.y2], [spike.x3, spike.y3], [spike.x1, spike.y1]])
    pygame.display.update()

    "Переход к окончанию игры или паузе в зависимости от числа очков"
    if not Player1.live or not Player2.live:
        if not Player1.live:
            Player2.wins += 1
        else:
            Player1.wins += 1
        if Player1.wins == 3 or Player2.wins == 3:
            game_over = True
            play = False
        else:
            game_break = True
            play = False



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
    "В зависимости от режима игры вызызает нужную функцию"
    global finished, stop, play, pause, game_over, not_started, Player1_wins, Player2_wins

    while not finished:

        if play and not not_started:
            "Основной цикл управление объектами во время игры"
            main_cycle()

            "Осуществляет переход в режим паузы"
            get_pause()

        if stop:
            "Реакция на действия игрока в режиме меню"
            menu()

        if play:
            "Реализует выбор игроками имён и переход в режим паузы"
            name_control()

        if pause:
            "Реагирует на действия игрока в режиме паузы"
            pause_control()

        if game_over:
            "Происходящее после окончания игры"
            game_over_control()
            start()

        if game_break:
            "Отвечает за происходящее между раундами"
            game_break_control()


def menu():
    "Реакция на действия игрока в режиме меню"
    global finished, stop, play, not_started, game_break

    "Создание кнопок"
    button_load = Button(300, 'Сontinue')
    button_play = Button(400, 'New Game')
    button_options = Button(500, 'Options')
    button_exit = Button(600, 'Exit')
    buttons = [button_load, button_play, button_options, button_exit]

    for button in buttons:
        image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text)
    pygame.display.update()
    "Обработка событий"
    for event in pygame.event.get():
        quit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            "Реакции на нажатия кнопок"
            if button_load.pressed(mouse_coords, button_load.coords1, button_load.coords3):
                if not_started == True:
                    pass
                else:
                    stop = False
                    play = True
            if button_play.pressed(mouse_coords, button_play.coords1, button_play.coords3):
                stop = False
                play = True
                not_started = True
                screen.fill(BLACK)
                start()
            if button_exit.pressed(mouse_coords, button_exit.coords1, button_exit.coords3):
                finished = True
            if button_options.pressed(mouse_coords, button_exit.coords1, button_exit.coords3):
                pass

def name_control():
    "Реализует выбор игроками имён"
    global finished, stop, play, not_started, pause
    if not_started:
        input_box1 = InputBox(400, 400, 100, 50)
        input = 1
        while input != 3:
            clock = pygame.time.Clock()
            "Присвоение игрокам имён"
            if input == 1:
                input_surf = pygame.font.Font(None, 60)
                input_text = input_surf.render('Enter the name of Player 1', True, RED)
                screen.blit(input_text, (275, 300))
                pygame.display.update()
            elif input == 2:
                input_surf = pygame.font.Font(None, 60)
                input_text = input_surf.render('Enter the name of Player 2', True, RED)
                screen.blit(input_text, (275, 300))
                pygame.display.update()
            "Реакции на действия игрока"
            for event in pygame.event.get():
                input_box1.handle_event(event, input)
                if event.type == pygame.QUIT:
                    input = 3
                    finished = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input += 1
            "Обновление состояния окошка"
            input_box1.update()
            input_box1.draw()

            pygame.display.flip()
            clock.tick(30)
        pygame.display.update()
        not_started = False


def get_pause():
    "Совершает переход в режим паузы во время игры"
    global play, pause, finished

    if not not_started and keyboard.is_pressed('Esc'):
        play = False
        pause = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


def pause_control():
    "Реагирует на действия игрока в режиме паузы"
    global finished, stop, play, pause
    "Создание кнопок"
    button_return = Button(400, 'Main Menu')
    button_back = Button(500, 'Back')
    buttons = [button_return, button_back]
    for button in buttons:
        image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text)
    pygame.display.update()
    for event in pygame.event.get():
        "Реакции на действия игрока"
        quit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            if button_return.pressed(mouse_coords, button_return.coords1, button_return.coords3):
                pause = False
                stop = True
                screen.fill(BLACK)
            if button_back.pressed(mouse_coords, button_back.coords1, button_back.coords3):
                pause = False
                play = True

def game_over_control():
    "Ответственна за происходящее после окончания игры"
    global finished, stop, play, pause, not_started, game_over

    play = False
    "Создание кнопок"
    button_end = Button(625, 'Main Menu')
    button_play_again = Button(725, 'Play again')
    buttons = [button_end, button_play_again]
    for button in buttons:
        image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text)
    pygame.display.update()

    "Создание надписей"
    over_surf = pygame.font.Font(None, 150)
    over_text = over_surf.render('Game Over', True, RED)
    screen.blit(over_text, (250, 150))

    score_surf = pygame.font.Font(None, 150)
    score_text = score_surf.render('Score:' + str(Player1.wins) + '-' + str(Player2.wins), True, BLUE)
    screen.blit(score_text, (260, 250))

    result_surf = pygame.font.Font(None, 75)

    if Player1.wins == 3:
        result_text = result_surf.render(Player2.name + ' ' + 'has won in this game!', True, ORANGE)
    else:
        result_text = result_surf.render(Player1.name + ' ' + 'has won in this game!', True, ORANGE)

    not_started = True
    screen.blit(result_text, (150, 400))

    start()

    "Обработка событий"
    for event in pygame.event.get():
        quit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            if button_end.pressed(mouse_coords, button_end.coords1, button_end.coords3):
                game_over = False
                stop = True
                screen.fill(BLACK)
            if button_play_again.pressed(mouse_coords, button_play_again.coords1, button_play_again.coords3):
                game_over = False
                play = True
                not_started = True
                screen.fill(BLACK)
                pygame.display.update()
                start()


def game_break_control():
    "Отвечает за происходящее между раундами"
    global finished, stop, play, pause, not_started, game_over, game_break

    play = False
    button_next_round = Button(525, 'Next round')
    button_Main_Menu = Button(625, 'Main Menu')
    buttons = [button_next_round, button_Main_Menu]
    for button in buttons:
        image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text)
    pygame.display.update()

    over_surf = pygame.font.Font(None, 150)
    over_text = over_surf.render('Score:' + str(Player1.wins) + '-' + str(Player2.wins), True, RED)
    screen.blit(over_text, (240, 250))
    result_surf = pygame.font.Font(None, 75)

    result_text = result_surf.render(Player2.name + ' ' + 'has won in this round!', True, ORANGE)
    screen.blit(result_text, (175, 400))

    for event in pygame.event.get():
        quit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            if button_next_round.pressed(mouse_coords, button_next_round.coords1, button_next_round.coords3):
                game_break = False
                play = True
                restart()
                screen.fill(BLACK)
                pygame.display.update()
            if button_Main_Menu.pressed(mouse_coords, button_Main_Menu.coords1, button_Main_Menu.coords3):
                game_break = False
                stop = True
                restart()
                screen.fill(BLACK)
                pygame.display.update()

def quit(event):
    "Проверяет, не нужно ли выйти из pygame"
    global finished
    if event.type == pygame.QUIT:
        finished = True
