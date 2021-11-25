import pygame
import pygame.draw
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


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
