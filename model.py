import math
import random


def tick(dt, controls):
    global Player1, Player2, spike
    dt += 1
    collide(Player1, Player2)
    Player1.wall()
    Player2.wall()
    Player1.death()
    Player2.death()
    Player1.move()
    Player2.move()
    Player1.death()
    Player2.death()
    Player1.wall()
    Player2.wall()
    Player1.newton(dt, [controls[0], controls[1]])
    Player2.newton(dt, [controls[2], controls[3]])
    return Player1, Player2, spike, dt


class Player:
    """
    Тип данных, описывающий одного из игроков
    """
    def __init__(self, xcord, ycord):
        self.live = True
        self.mass = 1
        self.color = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]
        self.size = 20
        self.x = xcord
        self.y = ycord
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay

    def newton(self, dt, controls):
        temp = field.engagement(self.mass, self.x, self.y, dt)
        self.ax = temp[0] + controls[0]
        self.ay = temp[1] + controls[1]

    def wall(self):
        if self.x - self.size < 0:
            self.vx = -self.vx
            self.x = self.size
        if self.size + self.x > 1024:
            self.vx = -self.vx
            self.x = 1024 - self.size
        if self.y - self.size < 0:
            self.vy = -self.vy
            self.y = self.size
        if self.size + self.y > 1024:
            self.vy = -self.vy
            self.y = 1024 - self.size

    def death(self):
        global spike
        self.live = not spike.penetration(self)


class Field:
    """
    Тип данных, описывающий свойства и структуру игрового поля
    """

    def evolve(self, x, y, dt):
        if x == 511 and y > 511:
            xproj = -0.3
            yproj = 0
        if x == 511 and y < 511:
            xproj = 0.3
            yproj = 0
        if y == 511 and x < 511:
            yproj = 0.3
            xproj = 0
        if y == 511 and x > 511:
            yproj = -0.3
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
        x = round(x)
        y = round(y)
        return [self.evolve(x, y, dt)[0] / m, self.evolve(x, y, dt)[1] / m]


class Spike:
    """
    Тип данных, отвечающий за взаимдействие игроков с шипами
    """
    def __init__(self):
        self.x1 = random.randint(300, 700)
        self.a = 20
        self.x3 = self.x1 + self.a
        self.x2 = self.x1 + self.a / 2
        self.y1 = random.randint(300, 700)
        self.y3 = self.y1
        self.y2 = self.y1 - math.sin(math.pi / 3) * self.a
        self.b12 = (self.y2 + self.y1 - math.sqrt(3) * (self.x1 + self.x2)) / 2
        self.b23 = (self.y3 + self.y2 + math.sqrt(3) * (self.x2 + self.x3)) / 2

    def penetration(self, player):
        d1 = math.sqrt((player.x - self.x1) ** 2 + (player.y - self.y1) ** 2)
        d2 = math.sqrt((player.x - self.x2) ** 2 + (player.y - self.y2) ** 2)
        d3 = math.sqrt((player.x - self.x3) ** 2 + (player.y - self.y3) ** 2)
        cos_psi1 = (d2 ** 2 - self.a ** 2 - d1 ** 2) / (-2 * d1 * self.a)
        cos_psi2 = (d3 ** 2 - self.a ** 2 - d2 ** 2) / (-2 * d2 * self.a)
        cos_psi3 = (d1 ** 2 - self.a ** 2 - d3 ** 2) / (-2 * d3 * self.a)
        Min_d = min(d1, d2, d3)
        if d1 <= player.size or d2 <= player.size or d3 <= player.size:
            return True
        if cos_psi1 >= 0 and d1 * math.sqrt(1 - cos_psi1 ** 2) <= player.size and d1 == Min_d:
            return True
        if cos_psi2 >= 0 and d2 * math.sqrt(1 - cos_psi2 ** 2) <= player.size and d2 == Min_d:
            return True
        if cos_psi3 >= 0 and d3 * math.sqrt(1 - cos_psi3 ** 2) <= player.size and d3 == Min_d:
            return True
        return False


def collide(player1, player2):
    if math.sqrt((player1.x - player2.x) ** 2 + (player1.y - player2.y) ** 2) <= player1.size + player2.size:
        m1 = player1.mass
        m2 = player2.mass
        v1x = player1.vx
        v1y = player1.vy
        v2x = player2.vx
        v2y = player2.vy
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
        player1.vx = v1x_true
        player1.vy = v1y_true
        player2.vx = v2x_true
        player2.vy = v2y_true


field = Field()
spike = Spike()
Player1 = Player(400, 800)
Player2 = Player(800, 800)
