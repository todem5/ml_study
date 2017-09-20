# Дана матрица (доска) m*n, заполненная какими-то случайными числами.
# Таксист едет из пункта (0,0) в (m,n) и имеет право совершать только 
# движения либо вниз, либо вправо.
# Перебрать все возможные маршруты и найти маршрут с наибольшей суммой

# Убираем самозакрывающиеся кавычки и скобки
from notebook.services.config import ConfigManager
c = ConfigManager()
c.update('notebook', {"CodeCell": {"cm_config": {"autoCloseBrackets": False}}})

import sys
import numpy as np # !!!!! -- Pandas
print(sys.version + "\n")

m = 4 # число строк - кодируем нулями
n = 5 # число столбцов - кодируем единицами

# Генерируем доску так.. 
desk = np.random.randint(low=0, high=100, size=(m,n))
print(desk) 
# ... или так ...
desk = np.random.choice([x for x in range(0,100,5)],n*m)
desk.resize(m,n)
print(desk)

# Создаём маршрут
#route = [0] * (m-1 + n-1) # Маршрут будет содержать n-1 единиц и m-1 нулей
# вариант в numpy
route = np.zeros(m-1 + n-1)
print(route)

### Функция перебора маршрутов
# По заданному маршруту генерирует следующий
def getNextRoute(route):
    perenos = True
    digit = route.size-1
    while (perenos):
        if (route[digit]==0):
            route[digit] = 1
            perenos = False
        else:
            route[digit] = 0
            perenos = True
            digit-=1
    return route 
    
# Тестируем функцию
for x in range(1, pow(2,m-1+n-1)+2):
    route = getNextRoute(route)
    print(route)

# Маршрут должен содержать m-1 нулей и n-1 единиц
def isRouteValid(route):
    zeros = 0
    ones = 0
    for i in route:
        if i==1:
            ones+=1
        else:
            zeros+=1
    return (zeros==m-1 and ones==n-1)
    
# Тестируем функцию
for x in range(1, pow(2,m-1+n-1)):
    route = getNextRoute(route)
    print(isRouteValid(route))
    
def calcRouteSum(route, desk):
    x = 0
    y = 0
    sum = 0
    for i in route:
        sum += desk[y,x] # desk[y][x]
        if i==0:
            y+=1
        else:
            x+=1
    sum += desk[y,x]
    return sum

# Тестируем функцию
for x in range(1, pow(2,m-1+n-1)):
    route = getNextRoute(route)
    if isRouteValid(route):
        sum = calcRouteSum(route,desk)
        print(route, sum)

route = np.zeros(m-1+n-1)
maxr = 0
for x in range(1, pow(2,m-1+n-1)):
    route = getNextRoute(route)
    if isRouteValid(route):
        sum = calcRouteSum(route,desk)
        if sum >= maxr:
            maxr = sum
            print(route, sum)
