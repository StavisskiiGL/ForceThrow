import math
import random
import colors
from colors import *

screen = pygame.display.set_mode((1024, 1024))
FPS = 30
pygame.init()


class InputBox:
    """Класс окна ввода игроком текста; x, y - координаты левого верхнего угла окна, w - ширина, h - высота"""
    def __init__(self, x, y, w, h, text=''):
        """Создание основных параметров окна"""
        self.FONT = pygame.font.Font(None, 50)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = manager.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, player_number, input_type):
        """Обработка событий, связанных с окном"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            "Если игрок щёлкнул по окну"
            if self.rect.collidepoint(event.pos):
                "Переключает активную переменную"
                self.active = not self.active
            else:
                self.active = False
            "Меняет цвет в зависимости от активности окна"
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    "Присвоение игрокам введённых имён"
                    if input_type == 'Name':
                        if player_number == 1:
                            manager.Player1.get_a_name(self.text)
                        elif player_number == 2:
                            manager.Player2.get_a_name(self.text)
                    elif input_type == 'Colour':
                        if player_number == 1:
                            manager.Player1.get_a_colour(self.text)
                        elif player_number == 2:
                            manager.Player2.get_a_colour(self.text)

                    self.text = ''
                    screen.fill((0, 0, 0))

                elif event.key == pygame.K_BACKSPACE:
                    "Убирает напечатанные символы при нажатии соответствующей клавиши"
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                "Обновление текста"
                self.txt_surface = manager.FONT.render(self.text, True, self.color)

    def update(self):
        """Удлиняет окно если текст слишком длинный"""
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        pygame.draw.polygon(screen, (0, 0, 0), [(400, 400), (1030, 400), (1030, 500), (400, 500)])
        "Отображает текст"
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        "Отображает окно"
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Big_Manager:
    """
    Класс, изменение параметров которого влечёт переключение между режимами
    игры (меню, собственно игры, паузы, положения между раундами); кроме того, на него ссылаются при необходимости
    узнать/изменить параметры объектов: Player1, Player2, field, spikes
    activate_sound - определяет, должен ли прозвучать звук нажатия кнопки.
    play, finished, pause, game_over, stop, not_started, game_break, game_break_counter, game_over_counter -
    отвечают за переключение функций модуля controller.
    field, Player1, Player2, star, sans, sans_picked_up, dtstar, dtsans, objects, spikes -
    содержат данные об основных объектах игры: поле, игроки, звезда, шипы
    """

    def __init__(self):
        self.play = False
        self.finished = False
        self.pause = False
        self.game_over = False
        self.game_over_counter = 0
        self.stop = True
        self.not_started = True
        self.game_break = False
        self.game_break_counter = 0
        self.dt = 0
        self.options = False
        self.field = Field()
        self.Player1 = Player(400, 800)
        self.Player2 = Player(800, 800)
        self.FONT = pygame.font.Font(None, 32)
        self.star = False
        self.sans = False
        self.sans_picked_up = False
        self.dtstar = 0
        self.dtsans = 0
        self.objects = [0, 0, 0]
        self.spikes = []

    def start(self):
        """Создание поля, шипов, игроков в начале игры"""

        self.field = Field()
        self.Player1 = Player(400, 800)
        self.Player2 = Player(800, 800)
        self.Player1.wins = 0
        self.Player2.wins = 0
        self.sans = False
        self.sans_picked_up = False
        self.objects = [0, 0, 0]
        self.star = False
        self.dtstar = 0
        self.dtsans = 0
        spike1 = Spike()
        spike2 = Spike()
        spike3 = Spike()
        self.spikes = [spike1, spike2, spike3]

    def restart(self):
        """Создание нового поля, новых шипов и откат к начальному состоянию игроков перед новым раундом"""

        self.field = Field()
        spike1 = Spike()
        spike2 = Spike()
        spike3 = Spike()
        self.spikes = [spike1, spike2, spike3]
        self.Player1.restart_parameters(400, 800)
        self.Player2.restart_parameters(800, 800)

    def tick(self, controls):
        """Основная функция, возвращающая состояние игроков, поля шипов и бонусов в каждый момент игры"""
        if self.dtstar == FPS * 12:
            self.objects[0] = StarPowerUp()
            self.star = True
            self.dtstar = -FPS * 6

        if self.dtsans == FPS * 14:
            self.objects[1] = Sans()
            self.sans = True
            self.dtsans = -FPS * 7
        self.dt += 1
        self.dtstar += 1
        self.dtsans += 1
        self.collide()
        self.Player1.wall()
        self.Player2.wall()
        self.collide()
        for i in self.spikes:
            self.Player1.death(i)
            self.Player2.death(i)
            if not self.Player1.live:
                self.Player1.dead = True
                self.Player1.live = True
            if not self.Player2.live:
                self.Player2.dead = True
                self.Player2.live = True

        self.collide()
        self.Player1.move()
        self.Player2.move()
        self.collide()
        if self.star:
            self.objects[0].pickup(self.Player1, self.dt)
            self.objects[0].pickup(self.Player2, self.dt)
        if self.Player1.invincible:
            self.Player1.star(self.dt)
        if self.Player2.invincible:
            self.Player2.star(self.dt)
        if self.sans:
            self.objects[1].pickup(self.Player1, self.dt)
            self.objects[1].pickup(self.Player2, self.dt)
        if self.Player1.immovable:
            self.Player1.sans(self.dt)
        if self.Player2.immovable:
            self.Player2.sans(self.dt)
        for i in self.spikes:
            self.Player1.death(i)
            self.Player2.death(i)
        self.collide()
        self.Player1.wall()
        self.Player2.wall()
        self.collide()
        self.Player1.newton(self.dt, [controls[0], controls[1]], [controls[2], controls[3]])
        self.Player2.newton(self.dt, [controls[2], controls[3]], [controls[0], controls[1]])
        self.collide()
        return self.Player1, self.Player2, self.spikes, self.field, self.dt, self.objects

    def collide(self):
        """Определяет результат столкновения между игроками"""
        if math.sqrt((self.Player1.x - self.Player2.x) ** 2 + (self.Player1.y - self.Player2.y) ** 2) <= self.Player1.size + self.Player2.size:
            if self.Player1.immovable or self.Player2.immovable:
                return
            if self.Player1.invincible:
                self.Player2.stardeath()
                return
            if self.Player2.invincible:
                self.Player1.stardeath()
                return
            m1 = self.Player1.mass
            m2 = self.Player2.mass
            v1x = self.Player1.vx
            v1y = self.Player1.vy
            v2x = self.Player2.vx
            v2y = self.Player2.vy
            vx_cm = (m1 * v1x + m2 * v2x) / (m1 + m2)
            vy_cm = (m1 * v1y + m2 * v2y) / (m1 + m2)
            v1x_cm = v1x - vx_cm
            v1y_cm = v1y - vy_cm
            v2x_cm = v2x - vx_cm
            v2y_cm = v2y - vy_cm
            v1x_true = -v1x_cm + vx_cm
            v1y_true = -v1y_cm + vy_cm
            v2x_true = -v2x_cm + vx_cm
            v2y_true = -v2y_cm + vy_cm
            self.Player1.vx = v1x_true
            self.Player1.vy = v1y_true
            self.Player2.vx = v2x_true
            self.Player2.vy = v2y_true


class Button:
    """Класс кнопки меню; j - координата по вертикали, name - текст внутри кнопки"""
    def __init__(self, j, name):
        self.coords1 = (400, j)
        self.coords2 = (650, j)
        self.coords3 = (650, j + 100)
        self.coords4 = (400, j + 100)
        self.text = name
        self.color = GREEN

    def pressed(self, mouse_coords, coords1, coords3):
        """Определяет, наведена ли мышь на кнопку"""

        if coords1[0] < mouse_coords[0] < coords3[0] and coords1[1] < mouse_coords[1] < coords3[1]:
            return True
        else:
            return False

    def change_color(self, mouse_coords, coords1, coords3):
        """Изменение цвета активированной кнопки"""
        if self.pressed(mouse_coords, coords1, coords3):
            self.color = BLUE
        else:
            self.color = GREEN


class StarPowerUp:
    """Класс звезды - усиления игры"""
    def __init__(self):
        """Создание геометрических характеристик звезды, определение её положения и цвета"""
        self.used = False
        self.xc = random.randint(200, 800)
        self.yc = random.randint(200, 800)
        self.r = 30
        self.a = math.sqrt(2 * self.r ** 2 - 2 * self.r ** 2 * math.cos(72/180 * math.pi)) * 1/2 / \
            math.sin(27 / 180 * math.pi)
        self.d = math.sqrt(self.a ** 2 + self.r ** 2 - 2 * self.r * self.a * math.cos(18 / 180 * math.pi))
        self.x1 = self.xc
        self.y1 = self.yc - self.r
        self.x2 = self.xc + self.d * math.sin(36 / 180 * math.pi)
        self.y2 = self.yc - self.d * math.cos(36 / 180 * math.pi)
        self.x3 = self.xc + self.r * math.sin(72 / 180 * math.pi)
        self.y3 = self.yc - self.r * math.cos(72 / 180 * math.pi)
        self.x4 = self.xc + self.d * math.sin(72 / 180 * math.pi)
        self.y4 = self.yc + self.d * math.cos(72 / 180 * math.pi)
        self.x5 = self.xc + self.r * math.sin(36 / 180 * math.pi)
        self.y5 = self.yc + self.r * math.cos(36 / 180 * math.pi)
        self.x6 = self.xc
        self.y6 = self.yc + self.d
        self.x7 = self.xc - self.r * math.sin(36 / 180 * math.pi)
        self.y7 = self.yc + self.r * math.cos(36 / 180 * math.pi)
        self.x8 = self.xc - self.d * math.sin(72 / 180 * math.pi)
        self.y8 = self.yc + self.d * math.cos(72 / 180 * math.pi)
        self.x9 = self.xc - self.r * math.sin(72 / 180 * math.pi)
        self.y9 = self.yc - self.r * math.cos(72 / 180 * math.pi)
        self.x10 = self.xc - self.d * math.sin(36 / 180 * math.pi)
        self.y10 = self.yc - self.d * math.cos(36 / 180 * math.pi)
        self.drawdata = [[self.x2, self.y2], [self.x3, self.y3], [self.x4, self.y4], [self.x5, self.y5],
                         [self.x6, self.y6], [self.x7, self.y7], [self.x8, self.y8], [self.x9, self.y9],
                         [self.x10, self.y10], [self.x1, self.y1]]
        self.color = [255, 255, 39]

    def pickup(self, player, dt):
        """Функция, регистрирующая использование звезды"""
        if math.sqrt((player.x - self.xc) ** 2 + (player.y - self.yc) ** 2) <= player.size + self.r and not self.used:
            player.star(dt)
            self.used = True


class Player:
    """
    Тип данных, описывающий одного из игроков
    x, y - координаты, vx, vy, ax, ay - составляющие скорости и ускорения по осям x и y
    mass - масса, wins - количество побед, dead - мёртв или нет, name - имя, color - цвет
    """
    def __init__(self, xcord, ycord):
        self.invincible = False
        self.immovable = False
        self.live = True
        self.mass = 1
        self.color = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]
        self.tempcolor = 0
        self.size = 50
        self.x = xcord
        self.y = ycord
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.t = 0
        self.t0 = 0
        self.name = 'Someone'
        self.wins = 0
        self.dead = False

    def get_a_name(self, name):
        """Присвоение имени игроку"""
        self.name = name

    def get_a_colour(self, color):
        """Присвоение цвета игроку"""
        if color == 'Red':
            self.color = colors.RED
        elif color == 'Green':
            self.color = colors.GREEN
        elif color == 'Blue':
            self.color = colors.BLUE
        elif color == 'Orange':
            self.color = colors.ORANGE
        elif color == 'White':
            self.color = colors.WHITE
        elif color == 'Random':
            self.color = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]
        else:
            self.color = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]

    def restart_parameters(self, xcord, ycord):
        """Возвращение к исходному состоянию при окончании раунда"""
        self.x = xcord
        self.y = ycord
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.t = 0
        self.t0 = 0
        self.dead = False

    def move(self):
        """Перемещение игрока"""
        if not self.immovable:
            self.x += self.vx
            self.y += self.vy
            self.vx += self.ax
            self.vy += self.ay

    def newton(self, dt, controls, sans_controls):
        """Воздействие на игрока силового поля"""
        if not manager.sans_picked_up:
            temp = manager.field.engagement(self.mass, int(self.x), int(self.y), dt)
            self.ax = temp[0] + controls[0]
            self.ay = temp[1] + controls[1]
        elif not self.immovable:
            self.ax = sans_controls[0] * 10
            self.ay = sans_controls[1] * 10

    def wall(self):
        """Столкновение игрока со стеной"""
        if self.x - self.size < 0:
            self.vx = -self.vx * 0.6
            self.x = self.size
        if self.size + self.x > 1024:
            self.vx = -self.vx * 0.6
            self.x = 1024 - self.size
        if self.y - self.size < 0:
            self.vy = -self.vy * 0.6
            self.y = self.size
        if self.size + self.y > 1024:
            self.vy = -self.vy * 0.6
            self.y = 1024 - self.size

    def death(self, spike):
        """Регистрация попадания на шип"""
        self.live = not spike.penetration(self)

    def stardeath(self):
        """Смерть от контакта с противником, взявшим бонус"""
        self.live = False

    def star(self, dt=1):
        """Взаимодействие со звездой"""
        if not self.invincible:
            self.tempcolor = self.color
            self.t0 = dt
        self.invincible = True
        if not self.t:
            self.t += 6
            return
        if dt % self.t:
            self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            self.t += 6
        if dt - self.t0 >= FPS * 6:
            self.invincible = False
            self.color = self.tempcolor
            manager.objects[0] = 0
            manager.star = False

    def sans(self, dt):
        """Взаимодействие с объектом класса Sans"""
        if not self.immovable:
            self.t0 = dt
        self.immovable = True
        if dt - self.t0 >= FPS * 7:
            self.immovable = False
            manager.objects[1] = 1
            manager.sans = False
            manager.sans_picked_up = False


class Sans:
    """
    Тип данных, отвечающий за усиление "SANS"
    """
    def __init__(self):
        self.used = False
        self.x = random.randint(200, 800)
        self.y = random.randint(200, 800)
        self.r = 80

    def pickup(self, player, dt):
        """Контакт игрока c Sans"""
        if math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2) <= player.size + self.r and not self.used:
            player.sans(dt)
            self.used = True
            manager.sans_picked_up = True


class Field:
    """
    Тип данных, описывающий свойства и структуру игрового поля
    """
    def evolve(self, x, y, dt):
        """Вычисление действующей на игрока силы в зависимости от его положения и момента времени"""
        if x == 511 and y > 511:
            xproj = -0.4
            yproj = 0
        if x == 511 and y < 511:
            xproj = 0.4
            yproj = 0
        if y == 511 and x < 511:
            yproj = 0.4
            xproj = 0
        if y == 511 and x > 511:
            yproj = -0.4
            xproj = 0
        if x < 511 and y < 511:
            rad_k = (y - 511) / (511 - x)
            force_k = (1 / rad_k)
            xproj = math.sqrt(1 / (force_k ** 2 + 1)) * 0.4
            yproj = math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.4
        if x < 511 and y > 511:
            rad_k = (y - 511) / (511 - x)
            force_k = (1 / rad_k)
            xproj = -math.sqrt(1 / (force_k ** 2 + 1)) * 0.4
            yproj = -math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.4
        if x > 511 and y < 511:
            rad_k = (y - 511) / (511 - x)
            force_k = (1 / rad_k)
            xproj = math.sqrt(1 / (force_k ** 2 + 1)) * 0.4
            yproj = math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.4
        if x > 511 and y > 511:
            rad_k = (y - 511) / (511 - x)
            force_k = (1 / rad_k)
            xproj = -math.sqrt(1 / (force_k ** 2 + 1)) * 0.4
            yproj = -math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.4

        return(xproj * math.cos(-0.05 * dt) + yproj * math.sin(-0.05 * dt),
               -xproj * math.sin(-0.05 * dt) + yproj * math.cos(-0.05 * dt))

    def engagement(self, m, x, y, dt):
        """Воздействие силового поля на игрока"""
        x = round(x)
        y = round(y)
        return [self.evolve(x, y, dt)[0] / m, self.evolve(x, y, dt)[1] / m]


class Spike:
    """
    Тип данных, отвечающий за взаимодействие игроков с шипами
    """
    def __init__(self):
        """Создание характеристик шипа: координаты на поле, длины сторон, углы между ними"""
        self.x1 = random.randint(300, 700)
        self.a = 60
        self.x3 = self.x1 + self.a
        self.x2 = self.x1 + self.a / 2
        self.y1 = random.randint(300, 700)
        self.y3 = self.y1
        self.y2 = self.y1 - math.sin(math.pi / 3) * self.a
        self.b12 = (self.y2 + self.y1 + math.sqrt(3) * (self.x1 + self.x2)) / 2
        self.b23 = (self.y3 + self.y2 - math.sqrt(3) * (self.x2 + self.x3)) / 2

    def penetration(self, player):
        """Фиксирует столкновение игрока с шипом"""
        if player.invincible:
            return False
        d1 = math.sqrt((player.x - self.x1) ** 2 + (player.y - self.y1) ** 2)
        d2 = math.sqrt((player.x - self.x2) ** 2 + (player.y - self.y2) ** 2)
        d3 = math.sqrt((player.x - self.x3) ** 2 + (player.y - self.y3) ** 2)
        cos_psi1_1 = (d2 ** 2 - self.a ** 2 - d1 ** 2) / (-2 * d1 * self.a)
        cos_psi2_2 = (d3 ** 2 - self.a ** 2 - d2 ** 2) / (-2 * d2 * self.a)
        cos_psi3_3 = (d1 ** 2 - self.a ** 2 - d3 ** 2) / (-2 * d3 * self.a)
        if d1 <= player.size or d2 <= player.size or d3 <= player.size:
            return True
        if self.y1 >= player.y >= player.x * math.sqrt(3) + self.b23 and d1 * math.sqrt(1 - cos_psi1_1 ** 2) <= player.size:
            return True
        if self.y1 >= player.y >= -player.x * math.sqrt(3) + self.b12 and d2 * math.sqrt(1 - cos_psi2_2 ** 2) <= player.size:
            return True
        if self.y1 <= player.y >= player.x * math.sqrt(3) + self.b23 and player.y >= -player.x * math.sqrt(3) + self.b12 and d3 * math.sqrt(1 - cos_psi3_3 ** 2) <= player.size:
            return True
        if self.y1 >= player.y >= player.x * math.sqrt(3) + self.b23 and player.y >= -player.x * math.sqrt(3) + self.b12:
            return True
        return False


manager = Big_Manager()
