from sympy import *
from sympy.geometry import Polygon, Point, Segment
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
    vertices = [Point(-a, 0)]

    # Вторая вершина на оси X
    vertices.append(Point(0, 0))

    # Центральный угол между сторонами многоугольника
    angle_step = 2 * pi / n
    alpha_init=(3*pi)/2-(angle_step/2)
    # Координаты центра описанной окружности
    R = a / (2 * sin(pi / n))
    Ry=sqrt(R**2-(a/2)**2)
    #print(R,Ry)

    # Вычисляем координаты оставшихся вершин
    for i in range(2, n):
        angle = alpha_init+ angle_step * i
        x = R * cos(angle) - a/2
        y = R * sin(angle) + Ry
        #\\print(angle, x, y)
        vertices.append(Point(x, y))

    return vertices


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

#сдвиг многоугольника на вектор
def shift_polygon(polygon, dx=0, dy=0):
    # Создаем вектор сдвига
    shift_vector = Matrix([dx, dy])

    # Применяем сдвиг ко всем точкам многоугольника
    shifted_polygon = [point + shift_vector for point in polygon]

    return shifted_polygon

# Функция для визуализации многоугольников с координатной сеткой
def plot_polygons(pre_inner_polygon, pre_outer_polygon):
    inner_polygon=Polygon(*pre_inner_polygon)
    outer_polygon=Polygon(*pre_outer_polygon)
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
a=sqrt(2)
b=sqrt(2)/3
outer_polygon=create_regular_polygon(a, 12)
inner_polygon = create_regular_polygon(b, 5) #этот экземпляр не меняется и его можно использовать для рассчёта поворотов
#сдвигаю
inner_polygon_shift=shift_polygon(inner_polygon, dx=b-a)

plot_polygons(inner_polygon_shift, outer_polygon)


"""
идея функции
подаём координату точки O (которая 0,0 на fix экземпляре)
пока что всё лежит на оси x
нужно рассчитать поворот относительно этой точки по ЧАСОВОЙ СТРЕЛКЕ до второй грани внешнего многоугольника
ответом должна быть координата точки (можно просто длину, потом всё равно переворачивать), в которую попадает o при вращении
нужно так же сделать проверку на то, что после этой процедуры не будет никаких лишних пересечений с внешним многоугольником
"""
def rotate(coord, inner_polygon, outer_polygon):



