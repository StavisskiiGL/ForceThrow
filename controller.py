import keyboard
from model import tick, Button, start, InputBox, screen, restart, manager
from view import *
from colors import BLACK, RED, BLUE, ORANGE
from soundtrack import Volume_control
import thorpy

clock = pygame.time.Clock()
pygame.display.update()
field_drawer = Drawer(screen)
drawer = Drawer(screen)
volume_control = Volume_control()


def controller():
    """В зависимости от режима игры, определяемого состоянием параметров
    объекта класса Big_Manager, вызызает нужную функцию"""

    pygame.mixer.music.set_volume(volume_control.music_volume)

    while not manager.finished:

        volume_control.music_control(manager)

        if manager.play and not manager.not_started:
            "Основной цикл управление объектами во время игры"
            control.main_cycle()

            "Осуществляет переход в режим паузы"
            control.get_pause()

        if manager.stop:
            "Реакция на действия игрока в режиме меню"
            control.menu()
            volume_control.sounds_control(manager)

        if manager.play:
            "Реализует выбор игроками имён и переход в режим паузы"
            control.name_control()

        if manager.pause:
            "Реагирует на действия игрока в режиме паузы"
            control.pause_control()
            volume_control.sounds_control(manager)

        if manager.game_over:
            "Происходящее после окончания игры"
            control.game_over_control()
            volume_control.sounds_control(manager)
            start()

        if manager.game_break:
            "Отвечает за происходящее между раундами"
            control.game_break_control()
            volume_control.sounds_control(manager)

        if manager.options:
            control.options_control(screen)


class Control:
    def __init__(self):
        self.name = 'controller'

    def main_cycle(self):
        """Основной цикл: управление объектами во время игры"""

        clock.tick(FPS)
        p1x, p1y = control.init_operate_p1()
        p2x, p2y = control.init_operate_p2()
        controls = [p1x, p1y, p2x, p2y]
        Player1, Player2, spike, field, manager.dt, objects = tick(manager.dt, controls)
        field_drawer.update(field, manager.dt)
        drawer.display_player(Player1)
        drawer.display_player(Player2)
        drawer.draw_score(Player1, Player2)

        if type(objects[0]) != type(1):
            print(objects[0])
            if not objects[0].used:
                pygame.draw.polygon(screen, objects[0].color, objects[0].drawdata)
        pygame.draw.polygon(screen, [255, 255, 255],
                            [[spike.x2, spike.y2], [spike.x3, spike.y3], [spike.x1, spike.y1]])

        if type(objects[1]) != type(1):
            if not objects[1].used:
                sans_image = pygame.image.load("Sans.png").convert_alpha()
                sans_image = pygame.transform.scale(sans_image, (objects[1].r, objects[1].r))
                screen.blit(sans_image, (objects[1].x, objects[1].y))

        pygame.display.update()

        "Переход к окончанию игры в зависимости от числа очков"
        if not Player1.live or not Player2.live:
            if not Player1.live:
                Player2.wins += 1
            else:
                Player1.wins += 1
            screen.fill(BLACK)
            pygame.display.update()
            control.get_over(Player1, Player2)

    def menu(self):
        """Реакция на действия игрока в режиме меню"""
        menu_image = pygame.image.load("Menu.png").convert_alpha()
        menu_image = pygame.transform.scale(menu_image, (1000, 1125))
        screen.blit(menu_image, (0, 0))
        "Создание кнопок"
        button_load = Button(100, 'Сontinue')
        button_play = Button(200, 'New Game')
        button_options = Button(300, 'Options')
        button_exit = Button(400, 'Exit')
        buttons = [button_load, button_play, button_options, button_exit]

        "Обработка событий"
        for event in pygame.event.get():
            control.quit(event)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = pygame.mouse.get_pos()
                "Реакции на нажатия кнопок"
                volume_control.activate_sound = True
                if button_load.pressed(mouse_coords, button_load.coords1, button_load.coords3):
                    if not manager.not_started:
                        manager.stop = False
                        manager.play = True
                        screen.fill(BLACK)
                        pygame.display.update()
                if button_play.pressed(mouse_coords, button_play.coords1, button_play.coords3):
                    manager.stop = False
                    manager.play = True
                    manager.not_started = True
                    screen.fill(BLACK)
                    pygame.display.update()
                    start()
                if button_exit.pressed(mouse_coords, button_exit.coords1, button_exit.coords3):
                    manager.finished = True
                if button_options.pressed(mouse_coords, button_options.coords1, button_options.coords3):
                    manager.options = True
                    manager.stop = False
                    screen.fill(BLACK)
                    pygame.display.update()
            if event.type == pygame.MOUSEMOTION:
                drawer.buttons_view(buttons)

    def name_control(self):
        """Реализует выбор игроками имён"""

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
                        if event.key == pygame.K_RETURN and input_box1.active:
                            input1 += 1
                "Обновление состояния окошка"
                input_box1.update()
                input_box1.draw()

                pygame.display.flip()
                clock.tick(30)
            screen.fill(BLACK)
            pygame.display.update()
            manager.not_started = False

    def get_pause(self):
        """Совершает переход в режим паузы во время игры"""

        if not manager.not_started and keyboard.is_pressed('Esc'):
            manager.play = False
            manager.pause = True
            button_return = Button(400, 'Main Menu')
            button_back = Button(500, 'Back')
            buttons = [button_return, button_back]
            drawer.buttons_view(buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manager.finished = True

    def init_operate_p1(self):
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

    def init_operate_p2(self):
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

    def get_over(self, player1, player2):
        """Фиксирует переход к окончанию игры"""

        if player1.wins == 3 or player2.wins == 3:
            manager.game_over = True
            manager.game_over_counter += 1
            manager.play = False
            demotivator_image = pygame.image.load("Demotivator.png").convert_alpha()
            demotivator_image = pygame.transform.scale(demotivator_image, (700, 600))
            screen.blit(demotivator_image, (150, 0))
            button_end = Button(625, 'Main Menu')
            button_play_again = Button(725, 'Play again')
            buttons = [button_end, button_play_again]
            drawer.buttons_view(buttons)
            "Создание надписей"
            score_surf = pygame.font.Font(None, 75)
            score_text = score_surf.render('Score:' + str(player1.wins) + '-' + str(player2.wins), True, BLUE)
            screen.blit(score_text, (100, 700))
            if player1.wins == 3:
                winner_color = player1.color
            else:
                winner_color = player2.color
            pygame.draw.circle(screen, winner_color, [500, 170], 50)
            pygame.display.update()

        else:
            manager.game_break = True
            manager.play = False
            round_image = pygame.image.load("ScreenBetweenTheRounds.png").convert_alpha()
            round_image = pygame.transform.scale(round_image, (1000, 800))
            screen.blit(round_image, (0, 100))
            button_next_round = Button(525, 'Next round')
            button_main_menu = Button(625, 'Main Menu')
            buttons = [button_next_round, button_main_menu]
            drawer.buttons_view(buttons)

            over_surf = pygame.font.Font(None, 150)
            over_text = over_surf.render('Score:' + str(player1.wins) + '-' + str(player2.wins), True, RED)
            screen.blit(over_text, (240, 250))
            result_surf = pygame.font.Font(None, 75)

            if not player1.live:
                result_text = result_surf.render(player2.name + ' ' + 'has won in this round!', True, ORANGE)
            else:
                result_text = result_surf.render(player1.name + ' ' + 'has won in this round!', True, ORANGE)
            screen.blit(result_text, (175, 400))
            pygame.display.update()

    def get_menu(self):
        """Отображение кнопок при переходе в режим меню"""
        menu_image = pygame.image.load("Menu.png").convert_alpha()
        menu_image = pygame.transform.scale(menu_image, (1000, 1125))
        screen.blit(menu_image, (0, 0))
        button_load = Button(100, 'Сontinue')
        button_play = Button(200, 'New Game')
        button_options = Button(300, 'Options')
        button_exit = Button(400, 'Exit')
        buttons = [button_load, button_play, button_options, button_exit]
        drawer.buttons_view(buttons)

    def pause_control(self):
        """Реагирует на действия игрока в режиме паузы"""

        "Создание кнопок"
        button_return = Button(400, 'Main Menu')
        button_back = Button(500, 'Back')
        buttons = [button_return, button_back]

        for event in pygame.event.get():
            "Реакции на действия игрока"
            control.quit(event)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = pygame.mouse.get_pos()
                volume_control.activate_sound = True

                if button_return.pressed(mouse_coords, button_return.coords1, button_return.coords3):
                    manager.pause = False
                    manager.stop = True
                    screen.fill(BLACK)
                    pygame.display.update()
                if button_back.pressed(mouse_coords, button_back.coords1, button_back.coords3):
                    manager.pause = False
                    manager.play = True
            if event.type == pygame.MOUSEMOTION:
                drawer.buttons_view(buttons)

    def game_over_control(self):
        """Ответственна за происходящее после окончания игры"""
        manager.play = False
        "Создание кнопок"
        button_end = Button(625, 'Main Menu')
        button_play_again = Button(725, 'Play again')
        buttons = [button_end, button_play_again]
        drawer.buttons_view(buttons)
        manager.not_started = True
        start()

        "Обработка событий"
        for event in pygame.event.get():
            control.quit(event)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = pygame.mouse.get_pos()
                volume_control.activate_sound = True

                if button_end.pressed(mouse_coords, button_end.coords1, button_end.coords3):
                    manager.game_over = False
                    manager.stop = True
                    screen.fill(BLACK)
                    pygame.display.update()
                    control.get_menu()
                if button_play_again.pressed(mouse_coords, button_play_again.coords1, button_play_again.coords3):
                    manager.game_over = False
                    manager.play = True
                    manager.not_started = True
                    screen.fill(BLACK)
                    pygame.display.update()
                    start()
            if event.type == pygame.MOUSEMOTION:
                drawer.buttons_view(buttons)

    def game_break_control(self):
        """Отвечает за происходящее между раундами"""

        manager.play = False
        button_next_round = Button(525, 'Next round')
        button_main_menu = Button(625, 'Main Menu')
        buttons = [button_next_round, button_main_menu]
        drawer.buttons_view(buttons)

        for event in pygame.event.get():
            control.quit(event)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = pygame.mouse.get_pos()
                volume_control.activate_sound = True
                "Реакция на нажатия кнопок"
                if button_next_round.pressed(mouse_coords, button_next_round.coords1, button_next_round.coords3):
                    manager.game_break = False
                    manager.play = True
                    restart()
                    screen.fill(BLACK)
                    pygame.display.update()
                if button_main_menu.pressed(mouse_coords, button_main_menu.coords1, button_main_menu.coords3):
                    manager.game_break = False
                    manager.stop = True
                    restart()
                    screen.fill(BLACK)
                    pygame.display.update()
                    control.get_menu()
            if event.type == pygame.MOUSEMOTION:
                """Отображение и окрашивание активированных кнопок"""
                drawer.buttons_view(buttons)

    def options_control(self, screen):
        """Реагирует на действия игрока при переходе в раздел меню "options"
        """
        menu, box = control.init_box()

        while manager.options:

            for event in pygame.event.get():
                "Реакция на действия игрока"
                menu.react(event)
                control.quit(event)
                if event.type == pygame.QUIT:
                    manager.options = False
            "Установление новых уровней громкости"
            volume_control.music_control(manager)
            volume_control.sounds_control(manager)

            "Обновление внешнего вида слайдеров"
            box.blit()
            box.update()

        "Переход обратно в меню"
        screen.fill(BLACK)
        pygame.display.update()
        control.get_menu()

    def slider_reaction(self, event, slider_music, slider_sounds):
        """Преобразует установленные на слайдерах значения в значения уровней громкости музыки и звуков"""

        if event.el == slider_music:
            new_volume = event.el.get_value() * 0.01
            volume_control.music_volume = new_volume
        elif event.el == slider_sounds:
            new_volume = event.el.get_value() * 0.01
            volume_control.sounds_volume = new_volume
            volume_control.sounds_control(manager)

    def init_box(self):
        """Создаёт слайдера контроля громкости музыки и звуков, кнопку возвращения в главное меню,
        описывает реакцию на связанные с ними действия игрока"""

        button_stop = thorpy.make_button("Main Menu", func=control.stop_options)
        button_stop.set_main_color((0, 255, 0))
        button_stop.set_size((300, 75))
        button_stop.set_font_size(40)

        slider_music = thorpy.SliderX(length=400, limvals=(0, 100), text="Music:", type_=int)
        slider_sounds = thorpy.SliderX(length=400, limvals=(0, 100), text="Sounds:", type_=int)

        "Установка слайдеров на текущий уровень громкости"
        slider_music.set_value(volume_control.music_volume * 100)
        slider_sounds.set_value(volume_control.sounds_volume * 100)

        box = thorpy.Box(elements=[button_stop, slider_music, slider_sounds])

        reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT, reac_func=control.slider_reaction,
                                   event_args={"id": thorpy.constants.EVENT_SLIDE},
                                   params={"slider_sounds": slider_sounds, "slider_music": slider_music},
                                   reac_name="my reaction to slide event")

        box.add_reaction(reaction)
        menu = thorpy.Menu(box)

        for element in menu.get_population():
            element.surface = screen

        box.set_topleft((300, 400))
        box.blit()
        box.update()

        return menu, box

    def quit(self, event):
        """Проверяет, не является ли событие "event" выходом из pygame"""
        if event.type == pygame.QUIT:
            manager.finished = True

    def stop_options(self):
        """Функция для кнопки "Main Menu в options, осуществляющая возвращение в главное меню"""
        volume_control.activate_sound = True
        manager.options = False
        manager.stop = True


control = Control()
