import math
temp = []
metric = []
for i in range(0, 1024):
    temp.append([1, 1])
for j in range(0, 1024):
     metric.append(temp)
for x in range(0, 1024):
    for y in range(0, 1024):
        if y != 511 and x != 511:
            metric[x][y][0] = metric[x][y][0] * (y - 511) / abs(y - 511)
            metric[x][y][1] = metric[x][y][1] * (511 - x) / abs(511 - x)
for x in range(0, 1024):
    for y in range(0, 1024):
        print(metric[x][y], " ", x, " ", y)
