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
    ax.plot(sqrt(-8*sqrt(5) - 3*sqrt(5 - sqrt(5))*sqrt(sqrt(5) + 5) - 4*sqrt(2)*sqrt(sqrt(5) + 3) + sqrt(5)*sqrt(5 - sqrt(5))*sqrt(sqrt(5) + 5) + 2*sqrt(10)*sqrt(sqrt(5) + 3) + 24)/(6*sqrt(5 - 2*sqrt(5))), 0, 'ro')
    plt.show()

#тест:
a=Symbol('a')
b=Symbol('b')

outer_polygon=create_regular_polygon(a, 12)
inner_polygon = create_regular_polygon(b, 5) #этот экземпляр не меняется и его можно использовать для рассчёта поворотов
#сдвигаю
inner_polygon_shift=shift_polygon(inner_polygon, dx=b-a)

#plot_polygons(inner_polygon_shift, outer_polygon)


"""
идея функции
подаём координату точки O (которая 0,0 на fix экземпляре)
пока что всё лежит на оси x
нужно рассчитать поворот относительно этой точки по ЧАСОВОЙ СТРЕЛКЕ до второй грани внешнего многоугольника
ответом должна быть координата точки (можно просто длину, потом всё равно переворачивать), в которую попадает o при вращении
нужно так же сделать проверку на то, что после этой процедуры не будет никаких лишних пересечений с внешним многоугольником

coord - просто число, так как смотрим по оси x
"""
def rotate(coord, inner_polygon, outer_polygon):
    #пояснение на пояснения\img.png
    x1_inner, y1_inner = inner_polygon[1]
    x2_inner, y2_inner = inner_polygon[2]
    x1_outer, y1_outer = outer_polygon[1]
    x2_outer, y2_outer = outer_polygon[2]

    cosa=-(Abs(x2_outer - x1_outer)/((x2_outer - x1_outer)**2 + (y2_outer - y1_outer)**2))
    #по Т. косинусов inner_2^2=x^2+(outer_1-coord)^2-2*x*(outer_1-coord)*cos(angle)
    x= symbols('x',positive=True)
    return {"x":(solve((x2_inner-x1_inner)**2+(y2_inner-y1_inner)**2-x**2-(x1_outer-coord)**2+2*x*cosa*Abs(x1_outer-coord), x, minimal=True )[0]), "cos":cosa]


# набор сторон внутреннего многоугольника
grans=[]
for i in range(0, len(inner_polygon)):
    if i!=len(inner_polygon)-1:
        #магия sympy для того, что бы выражение не тянулось на три строки
        grans.append((((inner_polygon[i][0]-inner_polygon[i+1][0])**2).simplify()+((inner_polygon[i][1]-inner_polygon[i+1][1])**2).simplify()).simplify())
    else:
        grans.append((((inner_polygon[i][0]-inner_polygon[0][0])**2).simplify()+((inner_polygon[i][1]-inner_polygon[0][1])**2).simplify()))




#реализуем деление отрезка в заданной пропорции
def div(inner_polygon, inner_polygon_shift, grans ,outer_polygon,cycle, lim_s):

    #lim_s - ограничение отношения полученное в прошлом цикле рекурсии
    #cycle - номер итерации рекурсии
    #масштабный коэфициент ещё не введен
    #длинна первой и второй внешней грани
    outer_now = (((outer_polygon[0][0]-outer_polygon[1][0])**2).simplify()+((outer_polygon[0][1]-outer_polygon[1][1])**2).simplify()).simplify()
    outer_next =(((outer_polygon[1][0]-outer_polygon[2][0])**2).simplify()+((outer_polygon[1][1]-outer_polygon[2][1])**2).simplify()).simplify()

    #от одного до 1,n поворотов на одной грани внешнего
    for i in range(0,len(grans)+1):
        if i==0:
            #s- оставшаеся растояние, которое потом пойдет в rotate и будет использоваться для коэфициента масштабирования. равно outer_now-inner_polygon_shift[0][0] - сумма grans от нуля до i
            s=outer_polygon
        else:
            # s- оставшаеся растояние, которое потом пойдет в rotate и будет использоваться для коэфициента масштабирования. равно outer_now-inner_polygon_shift[0][0] - сумма grans от нуля до i
            S=sum(grans[],)

    #в какой-то момент нужно выйти на рекурсию, предварительно повернув всё, кроме inner_polygon так, что бы повтроить всё ещё раз + что бы корректно работал rotate

