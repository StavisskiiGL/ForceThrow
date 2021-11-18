import math


def tick():
    global Player1, Player2
    collide(Player1, Player2)
    Player1.newton()
    Player2.newton()
    Player1.move()
    Player2.move()
    field.evolve()


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

    def newton(self):
        temp = Field.engagement(self.mass, self.x, self.y)
        self.ax = temp[0]
        self.ay = temp[1]


class Field:
    """
    Тип данных, описывающий свойства и структуру игрового поля
    """
    def __init__(self):
        temp = []
        self.metric = []
        for i in range(1, 1024):
            temp.append([0, 0])
        for j in range(1, 1024):
            self.metric.append(temp)
        for x in range(0, 1023):
            for y in range(0, 1023):
                if y != 511 and x != 511:
                    rad_k = (511 - y) / (511 - x)
                    force_k = abs(1 / rad_k)
                    if x < 511 and (y > 511):
                        self.metric[x][y][0] = math.sqrt(1 / (force_k ** 2 + 1))
                        self.metric[x][y][1] = math.sqrt(1 / (force_k ** 2 + 1)) * force_k
                    if x > 511 and y > 511:
                        self.metric[x][y][0] = math.sqrt(1 / (force_k ** 2 + 1))
                        self.metric[x][y][1] = math.sqrt(1 / (force_k ** 2 + 1)) * (-force_k)
                    if x < 511 and y < 511:
                        self.metric[x][y][0] = -math.sqrt(1 / (force_k ** 2 + 1))
                        self.metric[x][y][1] = math.sqrt(1 / (force_k ** 2 + 1)) * force_k
                    if x > 511 and (y < 511):
                        self.metric[x][y][0] = -math.sqrt(1 / (force_k ** 2 + 1))
                        self.metric[x][y][1] = math.sqrt(1 / (force_k ** 2 + 1)) * (-force_k)
                if x == 511:
                    if y > 511:
                        self.metric[x][y][0] = 1
                        self.metric[x][y][1] = 0
                    if y < 511:
                        self.metric[x][y][0] = -1
                        self.metric[x][y][1] = 0
                if y == 511:
                    if x > 511:
                        self.metric[x][y][0] = 0
                        self.metric[x][y][1] = -1
                    if x < 511:
                        self.metric[x][y][0] = 0
                        self.metric[x][y][1] = 1

    def evolve(self):
        for x in range(0, 1023):
            for y in range(0, 1023):
                if x != 511 and y != 511:
                    temp = self.metric[x][y][0]
                    self.metric[x][y][0] = self.metric[x][y][0] * math.cos(0.01) + self.metric[x][y][1] * math.sin(0.01)
                    self.metric[x][y][1] = -temp * math.sin(0.01) + self.metric[x][y][1] * math.cos(0.01)

    def engagement(self, m, x, y):
        return [self.metric[x][y][0] / m, self.metric[x][y][1] / m]


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
        v1_cm = v1x_cm ** 2 + v1y_cm ** 2
        v2_cm = v2x_cm ** 2 + v2y_cm ** 2
        px_cm = m1 * v1x_cm + m2 * v2x_cm
        py_cm = m1 * v1y_cm + m2 * v2y_cm
        k = (px_cm ** 2 + py_cm ** 2 + m1 ** 2 * v1_cm - v2_cm * m2 ** 2) / (2 * m1)
        d = 4 * (px_cm ** 2 * v1_cm / (py_cm ** 2) + v1_cm - k**2 / (py_cm ** 2))
        a = ((px_cm ** 2) / (py_cm ** 2) + 1)
        b = -2 * k * px_cm / (py_cm ** 2)
        result_v1x_1 = (-b + math.sqrt(d)) / (2 * a)
        result_v1y_1 = k / py_cm - (px_cm / py_cm) * result_v1x_1
        result_v1x_2 = (-b - math.sqrt(d)) / (2 * a)
        result_v1y_2 = k / py_cm - (px_cm / py_cm) * result_v1x_2
        if v2x_cm >= 0 and v2y_cm >= 0:
            if result_v1x_1 - v1x_cm >= 0 and result_v1y_1 - v1y_cm >= 0:
                true_v1x = result_v1x_1
                true_v1y = result_v1y_1
                true_v2x = (px_cm - true_v1x * m1) / m2
                true_v2y = (py_cm - m1 * true_v1y) / m2
                player1.vx = true_v1x
                player1.vy = true_v1y
                player2.vx = true_v2x
                player2.vy = true_v2y
                return
            elif result_v1x_2 - v1x_cm >= 0 and result_v1y_2 - v1y_cm >= 0:
                true_v1x = result_v1x_2
                true_v1y = result_v1y_2
                true_v2x = (px_cm - true_v1x * m1) / m2
                true_v2y = (py_cm - m1 * true_v1y) / m2
                player1.vx = true_v1x
                player1.vy = true_v1y
                player2.vx = true_v2x
                player2.vy = true_v2y
                return

        if v2x_cm >= 0 and v2y_cm <= 0:
            if result_v1x_1 - v1x_cm >= 0 and result_v1y_1 - v1y_cm <= 0:
                true_v1x = result_v1x_1
                true_v1y = result_v1y_1
                true_v2x = (px_cm - true_v1x * m1) / m2
                true_v2y = (py_cm - m1 * true_v1y) / m2
                player1.vx = true_v1x
                player1.vy = true_v1y
                player2.vx = true_v2x
                player2.vy = true_v2y
                return
            elif result_v1x_2 - v1x_cm >= 0 and result_v1y_2 - v1y_cm <= 0:
                true_v1x = result_v1x_2
                true_v1y = result_v1y_2
                true_v2x = (px_cm - true_v1x * m1) / m2
                true_v2y = (py_cm - m1 * true_v1y) / m2
                player1.vx = true_v1x
                player1.vy = true_v1y
                player2.vx = true_v2x
                player2.vy = true_v2y
                return

        if v2x_cm <= 0 and v2y_cm >= 0:
            if result_v1x_1 - v1x_cm <= 0 and result_v1y_1 - v1y_cm >= 0:
                true_v1x = result_v1x_1
                true_v1y = result_v1y_1
                true_v2x = (px_cm - true_v1x * m1) / m2
                true_v2y = (py_cm - m1 * true_v1y) / m2
                player1.vx = true_v1x
                player1.vy = true_v1y
                player2.vx = true_v2x
                player2.vy = true_v2y
                return
            elif result_v1x_2 - v1x_cm <= 0 and result_v1y_2 - v1y_cm >= 0:
                true_v1x = result_v1x_2
                true_v1y = result_v1y_2
                true_v2x = (px_cm - true_v1x * m1) / m2
                true_v2y = (py_cm - m1 * true_v1y) / m2
                player1.vx = true_v1x
                player1.vy = true_v1y
                player2.vx = true_v2x
                player2.vy = true_v2y

        if v2x_cm <= 0 and v2y_cm <= 0:
            if result_v1x_1 - v1x_cm <= 0 and result_v1y_1 - v1y_cm <= 0:
                true_v1x = result_v1x_1
                true_v1y = result_v1y_1
                true_v2x = (px_cm - true_v1x * m1) / m2
                true_v2y = (py_cm - m1 * true_v1y) / m2
                player1.vx = true_v1x
                player1.vy = true_v1y
                player2.vx = true_v2x
                player2.vy = true_v2y
                return
            elif result_v1x_2 - v1x_cm <= 0 and result_v1y_2 - v1y_cm <= 0:
                true_v1x = result_v1x_2
                true_v1y = result_v1y_2
                true_v2x = (px_cm - true_v1x * m1) / m2
                true_v2y = (py_cm - m1 * true_v1y) / m2
                player1.vx = true_v1x
                player1.vy = true_v1y
                player2.vx = true_v2x
                player2.vy = true_v2y
                return


field = Field()
Player1 = Player(200, 200)
Player2 = Player(300, 300)











