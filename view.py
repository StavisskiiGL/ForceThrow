import pygame
import pygame.draw
import math
from colors import BLACK, WHITE, GREEN

FPS = 30


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update(self, field, dt):
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


def display_player(screen, player):
    pygame.draw.circle(screen, player.color, (player.x, player.y), player.size)


def image_button(screen, coords1, coords2, coords3, coords4, name, color):
    pygame.draw.polygon(screen, WHITE, [coords1, coords2, coords3, coords4], 20)
    pygame.draw.polygon(screen, color, [coords1, coords2, coords3, coords4])
    text_surf = pygame.font.Font(None, 60)
    button_text = text_surf.render(name, True, (0, 0, 0))
    screen.blit(button_text, coords1)


def draw_score(screen, player1, player2):
    input_surf = pygame.font.Font(None, 60)
    input_text = input_surf.render(player1.name + ' ' + str(player1.wins) + '-' + str(player2.wins) + ' ' + player2.name
                                   , True, [255, 0, 0])
    screen.blit(input_text, (150, 150))
