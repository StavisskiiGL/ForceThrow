import pygame
import pygame.draw
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update(self, field):
        self.screen.fill(BLACK)
        for x in range(63, 960, 128):
            for y in range(63, 960, 128):
                angle = math.atan(field.metric[x][y][1] / field.metric[x][y][0])
                if field.metric[x][y][0] < 0:
                    angle += math.pi
                r = 50 * math.sqrt(field.metric[x][y][1] ** 2 + field.metric[x][y][0] ** 2)
                pygame.draw.line(self.screen, WHITE, (x - r * math.cos(angle), y - r * math.sin(angle)),
                                 (x + r * math.cos(angle), y + r * math.sin(angle)), 4)
                pygame.draw.line(self.screen, WHITE, (x + r * math.cos(angle), y + r * math.sin(angle)),
                                 (x - r * math.sin(angle), y + r * math.cos(angle)), 4)
                pygame.draw.line(self.screen, WHITE, (x + r * math.cos(angle), y + r * math.sin(angle)),
                                 (x + r * math.sin(angle), y - r * math.cos(angle)), 4)


def display_player(screen, color, player):
    pygame.draw.circle(screen, color, (player.x, player.y), player.size)
