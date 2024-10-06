import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import math


# МЕТОД ДИХОТОМИИ
# Вычисление нового интервала
def get_new_dichotomy_segment(equation, old_segment, x_values):
    x = sp.symbols('x')

    [a, b] = old_segment
    [x_1, x_2] = x_values

    value_1 = equation.subs({x: x_1})
    value_2 = equation.subs({x: x_2})

    if value_1 < value_2:
        b = x_2
    elif value_1 > value_2:
        a = x_1
    else:
        a = x_1
        b = x_2

    return [a, b]


# Реализация дихитомного метода
def dichotomy_method(equation, segment, epsilon):
    delta = epsilon / 2
    [a, b] = segment
    number_of_steps = 0

    while abs(a - b) >= epsilon:
        x_1 = (a + b - delta) / 2
        x_2 = (a + b + delta) / 2

        [a, b] = get_new_dichotomy_segment(equation, [a, b], [x_1, x_2])
        number_of_steps += 2

    return [a, b], number_of_steps


# МЕТОД ЗОЛОТОГО СЕЧЕНИЯ
UNDEFINED = 'undefined'


# Вычисляет значение левой точки
def calculate_left_gr(segment):
    [a, b] = segment
    value = a + (3 - math.sqrt(5)) / 2 * (b - a)

    return value


# Вычисляет значение правой точки
def calculate_right_gr(segment):
    [a, b] = segment
    value = a + (math.sqrt(5) - 1) / 2 * (b - a)

    return value


# Вычисляет границы нового отрезка
def get_new_segment(old_segment, x_values):
    [a, b] = old_segment
    [x_1, value_1], [x_2, value_2] = x_values

    if value_1 < value_2:
        b = x_2
        x_2 = x_1
        value_2 = value_1
        value_1 = UNDEFINED
        x_1 = calculate_left_gr([a, b])
    else:
        a = x_1
        x_1 = x_2
        value_1 = value_2
        value_2 = UNDEFINED
        x_2 = calculate_right_gr([a, b])

    return [a, b], [[x_1, value_1], [x_2, value_2]]


# Первый шаг алгоритма
def first_step_gr(equation, old_segment, x_values):
    x = sp.symbols('x')

    [x_1, x_2] = x_values

    value_1 = equation.subs({x: x_1})
    value_2 = equation.subs({x: x_2})

    [a, b], x_values = get_new_segment(old_segment, [[x_1, value_1], [x_2, value_2]])

    return [a, b], x_values


# Шаг алгоритма
def new_step_gr(equation, old_segment, x_values):
    x = sp.symbols('x')

    [x_1, value_1], [x_2, value_2] = x_values

    if value_1 == UNDEFINED:
        value_1 = equation.subs({x: x_1})

    if value_2 == UNDEFINED:
        value_2 = equation.subs({x: x_2})

    [a, b], x_values = get_new_segment(old_segment, [[x_1, value_1], [x_2, value_2]])

    return [a, b], x_values


# Реализация метода золотого сечения
def golden_ratio_method(equation, segment, epsilon):
    [a, b] = segment
    number_of_steps = 0

    x_1 = calculate_left_gr([a, b])
    x_2 = calculate_right_gr([a, b])

    [a, b], x_values = first_step_gr(equation, [a, b], [x_1, x_2])

    number_of_steps += 2

    while abs(a - b) >= epsilon:
        [a, b], x_values = new_step_gr(equation, [a, b], x_values)
        number_of_steps += 1

    return [a, b], number_of_steps


# ОТРИСОВКА ГРАФИКА ЗАВИСИМОСТЕЙ
def draw_comparing_plot(equation, segment):
    epsilon_values = 0.1 / (5 ** np.arange(20))
    dichotomy_steps_values = []
    golden_ratio_steps_values = []

    for epsilon in epsilon_values:
        _, dichotomy_step = dichotomy_method(equation, segment, epsilon)
        _, golden_ratio_step = golden_ratio_method(equation, segment, epsilon)

        dichotomy_steps_values.append(dichotomy_step)
        golden_ratio_steps_values.append(golden_ratio_step)

    dichotomy_steps_values = np.array(dichotomy_steps_values)
    golden_ratio_steps_values = np.array(golden_ratio_steps_values)

    plt.figure(figsize=(10, 5))
    plt.plot(epsilon_values, dichotomy_steps_values, label="Метод дихотомии", color="blue")
    plt.plot(epsilon_values, golden_ratio_steps_values, label="Метод золотого сечения", color="red")

    plt.title('Сравнение зависимоти количества вычислений функции от эпсилон')
    plt.xlabel('Значения эпсилон')
    plt.ylabel('Количество вычислений функции')
    plt.legend()
    plt.show()

    epsilon_log_values = np.log(epsilon_values)

    plt.figure(figsize=(10, 5))
    plt.plot(epsilon_log_values, dichotomy_steps_values, label="Метод дихотомии", color="blue")
    plt.plot(epsilon_log_values, golden_ratio_steps_values, label="Метод золотого сечения", color="red")

    plt.title('Сравнение зависимоти количества вычислений функции от логарифма эпсилон')
    plt.xlabel('Значения логарифма эпсилон')
    plt.ylabel('Количество вычислений функции')
    plt.legend()
    plt.show()


def task_1():
    # Вариант 8 (методы дихотомии, зотолое сечение)
    # Входные данные
    x = sp.symbols('x')
    y = 1/7 * x**7 - x**3 + 1/2*x**2 - x
    [a, b] = [1, 1.5]
    epsilon = 0.05

    dichotomy_result, dichotomy_steps = dichotomy_method(equation=y, segment=[a, b], epsilon=epsilon)
    golden_ratio_result, golden_ratio_steps = golden_ratio_method(equation=y, segment=[a, b], epsilon=epsilon)

    print("Методом дихотомии был найден следующий интервал, которому принадлежит минимум:")
    print(dichotomy_result)
    print("Заданная точность была достигнута за следующее количество шагов:")
    print(dichotomy_steps)
    print()
    print("Методом золотого сечения был найден следующий интервал, которому принадлежит минимум:")
    print(golden_ratio_result)
    print("Заданная точность была достигнута за следующее количество шагов:")
    print(golden_ratio_steps)

    draw_comparing_plot(equation=y, segment=[a, b])