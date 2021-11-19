import math


def tick(dt, controls):
    global Player1, Player2
    dt += 1
    collide(Player1, Player2)
    Player1.wall()
    Player2.wall()
    Player1.move()
    Player2.move()
    Player1.wall()
    Player2.wall()
    Player1.newton(dt, [controls[0], controls[1]])
    Player2.newton(dt, [controls[2], controls[3]])
    return Player1, Player2, dt


class Player:
    """
    Тип данных, описывающий одного из игроков
    """
    def __init__(self, xcord, ycord):
        self.mass = 1
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


class Field:
    """
    Тип данных, описывающий свойства и структуру игрового поля
    """
    def __init__(self):
        temp = []
        self.metric = []
        for i in range(0, 1024):
            temp.append([0, 0])
        for j in range(0, 1024):
            self.metric.append(temp)
        for x in range(0, 1024):
            for y in range(0, 1024):
                if y != 511 and x != 511:
                    rad_k = (511 - y) / (511 - x)
                    force_k = abs(1 / rad_k)
                    if x < 511:
                        self.metric[x][y][0] = math.sqrt(1 / (force_k ** 2 + 1)) * 0.3 * (y - 511) / abs(y - 511)
                        self.metric[x][y][1] = math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.3 * (x - 511) / abs(511 - x)
                    else:
                        self.metric[x][y][0] = math.sqrt(1 / (force_k ** 2 + 1)) * 0.3 * (y - 511) / abs(y - 511)
                        self.metric[x][y][1] = -math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.3 * (x - 511) / abs(511 - x)

    def evolve(self, x, y, dt):
        return(self.metric[x][y][0] * math.cos(0.01 * dt) + self.metric[x][y][1] * math.sin(0.01 * dt),
               -self.metric[x][y][0] * math.sin(0.01) + self.metric[x][y][1] * math.cos(0.01))

    def engagement(self, m, x, y, dt):
        x = round(x)
        y = round(y)
        return [self.evolve(x, y, dt)[0] / m, self.evolve(x, y, dt)[1] / m]


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
Player1 = Player(550, 550)
Player2 = Player(600, 600)
