import pygame
import keyboard
from model import tick, Button, start, InputBox, screen, restart, Manager
from view import *
from colors import BLACK, RED, GREEN, BLUE, ORANGE
from soundtrack import sounds_control, music_control
import thorpy
import numpy as np
import time

Player1 = 0
Player2 = 0

clock = pygame.time.Clock()
pygame.display.update()
field_drawer = Drawer(screen)
manager = Manager()
drawer = Drawer(screen)

def controller():
    "В зависимости от режима игры, определяемого состоянием параметров объекта класса Manager, вызызает нужную функцию"

    pygame.mixer.music.set_volume(manager.music_volume)

    while not manager.finished:

        music_control(manager)

        if manager.play and not manager.not_started:
            "Основной цикл управление объектами во время игры"
            main_cycle()

            "Осуществляет переход в режим паузы"
            get_pause()

        if manager.stop:
            "Реакция на действия игрока в режиме меню"
            menu()
            sounds_control(manager)

        if manager.play:
            "Реализует выбор игроками имён и переход в режим паузы"
            name_control()

        if manager.pause:
            "Реагирует на действия игрока в режиме паузы"
            pause_control()
            sounds_control(manager)

        if manager.game_over:
            "Происходящее после окончания игры"
            game_over_control()
            sounds_control(manager)
            start()

        if manager.game_break:
            "Отвечает за происходящее между раундами"
            game_break_control()
            sounds_control(manager)

        if manager.options:
            options_control(screen)

def main_cycle():
    "Основной цикл: управление объектами во время игры"
    global Player1, Player2
    clock.tick(FPS)
    p1x, p1y = init_operate_p1()
    p2x, p2y = init_operate_p2()
    controls = [p1x, p1y, p2x, p2y]
    Player1, Player2, spike, field, manager.dt, objects = tick(manager.dt, controls)
    field_drawer.update(field, manager.dt)
    display_player(screen, Player1)
    display_player(screen, Player2)
    draw_score(screen, Player1, Player2)

    if type(objects[0]) != type(1):
        print(objects[0])
        if not objects[0].used:
            pygame.draw.polygon(screen, objects[0].color, objects[0].drawdata)
    pygame.draw.polygon(screen, [255, 255, 255],
                        [[spike.x2, spike.y2], [spike.x3, spike.y3], [spike.x1, spike.y1]])
    pygame.display.update()

    "Переход к окончанию игры в зависимости от числа очков"
    if not Player1.live or not Player2.live:
        if not Player1.live:
            Player2.wins += 1
        else:
            Player1.wins += 1
        screen.fill(BLACK)
        pygame.display.update()
        get_over(Player1, Player2)

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

def menu():
    "Реакция на действия игрока в режиме меню"

    "Создание кнопок"
    button_load = Button(300, 'Сontinue')
    button_play = Button(400, 'New Game')
    button_options = Button(500, 'Options')
    button_exit = Button(600, 'Exit')
    buttons = [button_load, button_play, button_options, button_exit]

    "Обработка событий"
    for event in pygame.event.get():
        quit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            "Реакции на нажатия кнопок"
            manager.activate_sound = True
            if button_load.pressed(mouse_coords, button_load.coords1, button_load.coords3):
                if manager.not_started == True:
                    pass
                else:
                    manager.stop = False
                    manager.play = True
                    screen.fill(BLACK)
                    pygame.display.update()
            if button_play.pressed(mouse_coords, button_play.coords1, button_play.coords3):
                manager.stop = False
                manager.play = True
                manager.not_started = True
                screen.fill(BLACK)
                start()
            if button_exit.pressed(mouse_coords, button_exit.coords1, button_exit.coords3):
                manager.finished = True
            if button_options.pressed(mouse_coords, button_options.coords1, button_options.coords3):
                manager.options = True
                manager.stop = False
                screen.fill(BLACK)
                pygame.display.update()
        if event.type == pygame.MOUSEMOTION:
            Button.buttons_view(buttons, screen)

def name_control():
    "Реализует выбор игроками имён"
    if manager.not_started:
        input_box1 = InputBox(400, 400, 100, 50)
        input1 = 1
        while input1 != 5:
            clock = pygame.time.Clock()
            "Присвоение игрокам имён"
            if input1 == 1:
                input_surf = pygame.font.Font(None, 60)
                input_text = input_surf.render('Enter the name of Player 1', True, RED)
                screen.blit(input_text, (275, 300))
                pygame.display.update()
            elif input1 == 2:
                input_surf = pygame.font.Font(None, 60)
                input1_text = input_surf.render('Enter Color of Player 1', True, RED)
                screen.blit(input1_text, (275, 300))
                input_surf = pygame.font.Font(None, 40)
                input1_text = input_surf.render('Acceptable Colors: Red, Green, Orange, Blue, White, Random', True,
                                                WHITE)
                screen.blit(input1_text, (100, 600))
                pygame.display.update()
            elif input1 == 3:
                input_surf = pygame.font.Font(None, 60)
                input_text = input_surf.render('Enter the name of Player 2', True, RED)
                screen.blit(input_text, (275, 300))
                pygame.display.update()
            elif input1 == 4:
                input_surf = pygame.font.Font(None, 60)
                input1_text = input_surf.render('Enter Color of Player 2', True, RED)
                screen.blit(input1_text, (275, 300))
                input_surf = pygame.font.Font(None, 40)
                input1_text = input_surf.render('Acceptable Colors: Red, Green, Orange, Blue, White, Random', True,
                                                WHITE)
                screen.blit(input1_text, (100, 600))
                pygame.display.update()
            "Реакции на действия игрока"
            for event in pygame.event.get():
                if input1 % 2 == 0:
                    input_type = 'Colour'
                else:
                    input_type = 'Name'
                if input1 < 3:
                    player_num = 1
                else:
                    player_num = 2
                input_box1.handle_event(event, player_num, input_type)
                if event.type == pygame.QUIT:
                    input1 = 5
                    manager.finished = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input1 += 1
            "Обновление состояния окошка"
            input_box1.update()
            input_box1.draw()

            pygame.display.flip()
            clock.tick(30)
        screen.fill(BLACK)
        pygame.display.update()
        manager.not_started = False

def get_pause():
    "Совершает переход в режим паузы во время игры"

    if not manager.not_started and keyboard.is_pressed('Esc'):
        manager.play = False
        manager.pause = True
        button_return = Button(400, 'Main Menu')
        button_back = Button(500, 'Back')
        buttons = [button_return, button_back]

        for button in buttons:
            Button.image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text,
                         button.color)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            manager.finished = True

def get_over(Player1, Player2):
    #Фиксирует окончание игры
    if Player1.wins == 3 or Player2.wins == 3:
        manager.game_over = True
        manager.play = False
        button_end = Button(625, 'Main Menu')
        button_play_again = Button(725, 'Play again')
        buttons = [button_end, button_play_again]
        for button in buttons:
            Button.image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text,
                         button.color)
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
        screen.blit(result_text, (150, 400))

        pygame.display.update()
    else:
        manager.game_break = True
        manager.play = False

        button_next_round = Button(525, 'Next round')
        button_Main_Menu = Button(625, 'Main Menu')
        buttons = [button_next_round, button_Main_Menu]
        for button in buttons:
            Button.image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text,
                         button.color)
        over_surf = pygame.font.Font(None, 150)
        over_text = over_surf.render('Score:' + str(Player1.wins) + '-' + str(Player2.wins), True, RED)
        screen.blit(over_text, (240, 250))
        result_surf = pygame.font.Font(None, 75)

        if not Player1.live:
            result_text = result_surf.render(Player2.name + ' ' + 'has won in this round!', True, ORANGE)
        elif not Player2.live:
            result_text = result_surf.render(Player1.name + ' ' + 'has won in this round!', True, ORANGE)

        screen.blit(result_text, (175, 400))
        pygame.display.update()

def get_menu():
    "Осуществляет переход в режим меню"
    button_load = Button(300, 'Сontinue')
    button_play = Button(400, 'New Game')
    button_options = Button(500, 'Options')
    button_exit = Button(600, 'Exit')
    buttons = [button_load, button_play, button_options, button_exit]

    for button in buttons:
        Button.image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text, button.color)
    pygame.display.update()

def pause_control():
    "Реагирует на действия игрока в режиме паузы"

    "Создание кнопок"
    button_return = Button(400, 'Main Menu')
    button_back = Button(500, 'Back')
    buttons = [button_return, button_back]

    for event in pygame.event.get():
        "Реакции на действия игрока"
        quit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            manager.activate_sound = True

            if button_return.pressed(mouse_coords, button_return.coords1, button_return.coords3):
                manager.pause = False
                manager.stop = True
                screen.fill(BLACK)
                pygame.display.update()
            if button_back.pressed(mouse_coords, button_back.coords1, button_back.coords3):
                manager.pause = False
                manager.play = True
        if event.type == pygame.MOUSEMOTION:
            Button.buttons_view(buttons, screen)

def game_over_control():
    "Ответственна за происходящее после окончания игры"
    manager.play = False
    "Создание кнопок"
    button_end = Button(625, 'Main Menu')
    button_play_again = Button(725, 'Play again')
    buttons = [button_end, button_play_again]
    for button in buttons:
        Button.image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text, button.color)

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

    manager.not_started = True
    screen.blit(result_text, (150, 400))

    start()

    "Обработка событий"
    for event in pygame.event.get():
        quit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            manager.activate_sound = True

            if button_end.pressed(mouse_coords, button_end.coords1, button_end.coords3):
                manager.game_over = False
                manager.stop = True
                screen.fill(BLACK)
                pygame.display.update()
                get_menu()
            if button_play_again.pressed(mouse_coords, button_play_again.coords1, button_play_again.coords3):
                manager.game_over = False
                manager.play = True
                manager.not_started = True
                screen.fill(BLACK)
                pygame.display.update()
                start()
        if event.type == pygame.MOUSEMOTION:
            Button.buttons_view(buttons, screen)

def game_break_control():
    "Отвечает за происходящее между раундами"

    manager.play = False
    button_next_round = Button(525, 'Next round')
    button_Main_Menu = Button(625, 'Main Menu')
    buttons = [button_next_round, button_Main_Menu]
    for button in buttons:
        Button.image_button(screen, button.coords1, button.coords2, button.coords3, button.coords4, button.text, button.color)

    over_surf = pygame.font.Font(None, 150)
    over_text = over_surf.render('Score:' + str(Player1.wins) + '-' + str(Player2.wins), True, RED)
    screen.blit(over_text, (240, 250))
    result_surf = pygame.font.Font(None, 75)

    if not Player1.live:
        result_text = result_surf.render(Player2.name + ' ' + 'has won in this round!', True, ORANGE)
    elif not Player2.live:
        result_text = result_surf.render(Player1.name + ' ' + 'has won in this round!', True, ORANGE)

    screen.blit(result_text, (175, 400))

    for event in pygame.event.get():
        quit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            manager.activate_sound = True

            if button_next_round.pressed(mouse_coords, button_next_round.coords1, button_next_round.coords3):
                manager.game_break = False
                manager.play = True
                restart()
                screen.fill(BLACK)
                pygame.display.update()
            if button_Main_Menu.pressed(mouse_coords, button_Main_Menu.coords1, button_Main_Menu.coords3):
                manager.game_break = False
                manager.stop = True
                restart()
                screen.fill(BLACK)
                pygame.display.update()
                get_menu()
        if event.type == pygame.MOUSEMOTION:
            #Отображение и окрашивание активированных кнопок
            Button.buttons_view(buttons, screen)


def slider_to_real(val):
    return (0.01 * val)


def slider_music_reaction(event):
    manager.music_volume = slider_to_real(event.el.get_value())

def slider_sounds_reaction(event):
    manager.sounds_volume = slider_to_real(event.el.get_value())


def options_control(screen):
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    button_return = Button(500, 'Main Menu')
    buttons = [button_return]
    Button.image_button(screen, button_return.coords1, button_return.coords2, button_return.coords3, button_return.coords4, button_return.text, button_return.color)
    pygame.display.update()
    menu, box = init_box(screen, "Music")

    while manager.options:
        for event in pygame.event.get():
            menu.react(event)

            quit(event)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = pygame.mouse.get_pos()
                "Реакции на нажатия кнопок"
                manager.activate_sound = True
                if button_return.pressed(mouse_coords, button_return.coords1, button_return.coords3):
                    manager.options = False
                    manager.stop = True
                    screen.fill(BLACK)
                    pygame.display.update()
            if event.type == pygame.MOUSEMOTION:
                Button.buttons_view(buttons, screen)

        music_control(manager)
        sounds_control(manager)
        screen.fill(BLACK)
        drawer.update_options(box)

    screen.fill(BLACK)
    pygame.display.update()
    get_menu()

def init_box(screen, type):
    slider = thorpy.SliderX(300, (0, 100), type)
    if type == "Music":
        slider.user_func = slider_music_reaction
        topleft = 400
    else:
        slider.user_func = slider_sounds_reaction
        topleft = 450
    box = thorpy.Box(elements=[
        slider])
    reaction1 = thorpy.Reaction(reacts_to = thorpy.constants.THORPY_EVENT,
                                reac_func = slider.user_func,
                                event_args = {"id": thorpy.constants.EVENT_SLIDE},
                                params = {},
                                reac_name = "slider_music_reaction")

    box.add_reaction(reaction1)

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((300, topleft))
    box.blit()
    box.update()
    return menu, box

def quit(event):
    "Проверяет, не нужно ли выйти из pygame"
    if event.type == pygame.QUIT:
        manager.finished = True
