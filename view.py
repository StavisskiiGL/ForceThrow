import pygame
import pygame.draw
import math

FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (124,252, 0)


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

def image_button(screen, coords1, coords2, coords3, coords4, name):
    pygame.draw.polygon(screen, WHITE, [coords1, coords2, coords3, coords4], 20)
    pygame.draw.polygon(screen, GREEN, [coords1, coords2, coords3, coords4])
    text_surf = pygame.font.Font(None, 60)
    button_text = text_surf.render(name, True, (0, 0, 0))
    screen.blit(button_text, coords1)