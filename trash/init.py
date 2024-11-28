from sympy import *
from sympy.geometry import Polygon, Point
import matplotlib.pyplot as plt

# Функция для создания правильного многоугольника
def create_regular_polygon(a, n):
    """
    Создаёт правильный n-угольник с одной вершиной в (0, 0) и одной стороной на оси X.
    :param a: длина стороны (символьная переменная)
    :param n: количество сторон (целое число)
    :return: объект Polygon из sympy
    """
    # Начальная вершина в (0, 0)
    vertices = [Point(0, 0)]

    # Вторая вершина на оси X
    vertices.append(Point(a, 0))

    # Центральный угол между сторонами многоугольника
    angle_step = 2 * pi / n
    alpha_init=(3*pi)/2-(angle_step/2)
    # Координаты центра описанной окружности
    R = a / (2 * sin(pi / n))
    Ry=(R**2-(a/2)**2)**0.5
    #print(R,Ry)

    # Вычисляем координаты оставшихся вершин
    for i in range(2, n):
        angle = alpha_init+ angle_step * i
        x = R * cos(angle) + a/2
        y = R * sin(angle) + Ry
        #print(angle, x, y)
        vertices.append(Point(x, y))

    return Polygon(*vertices)


# Функция для создания произвольного многоугольника по массиву координат
def create_custom_polygon(coords):
    """
    Создаёт произвольный многоугольник по массиву символьных координат.
    Пример массива: coords = [(x1, y1), (x2, y2), ..., (xn, yn)]
    :param coords: массив кортежей с координатами вершин
    :return: объект Polygon из sympy
    """
    vertices = [Point(x, y) for x, y in coords]
    return Polygon(*vertices)


# Функция для проверки, что внутренний многоугольник полностью лежит во внешнем
def is_polygon_inside(inner_polygon, outer_polygon):
    for vertex in inner_polygon.vertices:
        if not outer_polygon.encloses_point(vertex):
            return False
    return True


# Функция для визуализации многоугольников с координатной сеткой
def plot_polygons(inner_polygon, outer_polygon):
    fig, ax = plt.subplots()

    # Внешний многоугольник
    outer_x, outer_y = zip(*[(p.x.evalf(), p.y.evalf()) for p in outer_polygon.vertices + [outer_polygon.vertices[0]]])
    ax.plot(outer_x, outer_y, 'b-', label='Внешний многоугольник')

    # Внутренний многоугольник
    inner_x, inner_y = zip(*[(p.x.evalf(), p.y.evalf()) for p in inner_polygon.vertices + [inner_polygon.vertices[0]]])
    ax.plot(inner_x, inner_y, 'r-', label='Внутренний многоугольник')

    # Настройки отображения
    ax.legend()
    ax.set_aspect('equal')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)  # Координатная сетка
    ax.axhline(y=0, color='black', linewidth=0.8)  # Ось X
    ax.axvline(x=0, color='black', linewidth=0.8)  # Ось Y
    plt.show()

#тест:
# a=sqrt(2)
# b=sqrt(2)/3
a=3
b=1
outer_polygon=create_regular_polygon(a, 7)
inner_polygon = create_regular_polygon(b, 5)
plot_polygons(inner_polygon, outer_polygon)