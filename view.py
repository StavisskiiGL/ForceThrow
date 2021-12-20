import pygame
import pygame.draw
import math
from colors import BLACK, WHITE

FPS = 30


class Drawer:
    """Класс, осуществляющий отрисовку объектов на поле"""
    def __init__(self, screen):
        self.screen = screen

    def update(self, field, dt):
        """Функция отображения силового поля"""
        self.screen.fill(BLACK)
        for x in range(63, 960, 128):
            for y in range(63, 960, 128):
                xproj, yproj = field.evolve(x, y, dt)
                angle = math.atan(yproj / xproj)
                if xproj < 0:
                    angle += math.pi
                r = 50 * math.sqrt(yproj ** 2 + xproj ** 2)
                pygame.draw.line(self.screen, WHITE, (x - r * math.cos(angle), y - r * math.sin(angle)),
                                 (x + r * math.cos(angle), y + r * math.sin(angle)), 4)
                pygame.draw.line(self.screen, WHITE, (x + r * math.cos(angle), y + r * math.sin(angle)),
                                 (x - r * math.sin(angle), y + r * math.cos(angle)), 4)
                pygame.draw.line(self.screen, WHITE, (x + r * math.cos(angle), y + r * math.sin(angle)),
                                 (x + r * math.sin(angle), y - r * math.cos(angle)), 4)

    def display_player(self, player):
        """Функция отображения игрока на поле"""
        pygame.draw.circle(self.screen, player.color, (player.x, player.y), player.size)

    def draw_score(self, player1, player2):
        """Вывод счёта на экран"""
        input_surf = pygame.font.Font(None, 60)
        input_text = input_surf.render(player1.name + ' ' + str(player1.wins) + '-' + str(player2.wins) + ' ' +
                                       player2.name, True, [255, 0, 0])
        self.screen.blit(input_text, (150, 150))

    def buttons_view(self, buttons):
        """Комбинация операций отображения объектов класса Button и их окраски"""
        mouse_coords = pygame.mouse.get_pos()
        for button in buttons:
            button.change_color(mouse_coords, button.coords1, button.coords3)
            self.image_button(button.coords1, button.coords2,
                                button.coords3, button.coords4, button.text, button.color)
        pygame.display.update()

    def image_button(self, coords1, coords2, coords3, coords4, name, color):
        """Отображение объекта класса Button"""
        pygame.draw.polygon(self.screen, WHITE, [coords1, coords2, coords3, coords4], 20)
        pygame.draw.polygon(self.screen, color, [coords1, coords2, coords3, coords4])
        text_surf = pygame.font.Font(None, 60)
        button_text = text_surf.render(name, True, (0, 0, 0))
        self.screen.blit(button_text, coords1)
