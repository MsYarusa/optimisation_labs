import numpy as np
import sympy as sp


def get_new_segment(equation, old_segment, x_values):
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


def dichotomy_method(equation, segment, epsilon):
    delta = epsilon / 2
    [a, b] = segment
    number_of_steps = 0

    while abs(a - b) > epsilon:
        x_1 = (a + b - delta) / 2
        x_2 = (a + b + delta) / 2

        [a, b] = get_new_segment(equation, [a, b], [x_1, x_2])
        number_of_steps += 1

    return [a, b], number_of_steps


def task_1():
    # Вариант 8 (методы дихотомии, зотолое сечение)
    # Входные данные
    x = sp.symbols('x')
    y = 1/7 * x**7 - x**3 + 1/2*x**2 - x
    [a, b] = [1, 1.5]
    epsilon = 0.05

    dichotomy_result, dichotomy_steps = dichotomy_method(equation=y, segment=[a, b], epsilon=epsilon)

    print(dichotomy_result, dichotomy_steps)
