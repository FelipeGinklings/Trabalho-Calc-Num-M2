# %%
import math
from typing import Tuple
from functools import reduce
from functools import singledispatch


# %%
def z(x: float, x0: float, h: float):
    return x - x0 / h


# %%
# Regra dos Trapézios
def I_trapezoid(h: float, y: float):
    return (h / 2) * (y)


# %%
# Método de Simpson
def I_Simpson(h: float, y: float):
    return (h / 3) * (y)


# %%
def _ensure_int(value, name: str) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    raise TypeError(f"{name} must be an integer (got {type(value).__name__})")


# %%
# Regra dos Trapézios resultado
def result_I_trapezoid_with_expression(
    expression: object,
    interval: tuple,
    weight: int = 10000,
) -> float:
    if not callable(expression):
        raise TypeError("Expression must be callable")
    start = interval[0] * weight
    end = interval[1] * weight
    step = interval[2] * weight
    # ensure start, end and step are integers (allow float values that are whole numbers)
    start = _ensure_int(start, "start")
    end = _ensure_int(end, "end")
    step = _ensure_int(step, "step")
    # sample interior points (normalized by weight)
    y = [expression(x / weight) * 2 for x in range(start + step, end, step)]
    # include endpoints
    y.insert(0, expression(start / weight))
    y.append(expression(end / weight))
    return I_trapezoid(step / weight, sum(y))


# Regra dos Trapézios resultado
def result_I_trapezoid_with_y_list(y_list: list, h: int) -> float:
    doubled_y_values = [value * 2 for value in y_list]
    # include endpoints
    doubled_y_values.append(y_list[0])
    doubled_y_values.append(y_list[-1])
    return I_trapezoid(h, sum(doubled_y_values))


if __name__ == "__main__":
    print(
        result_I_trapezoid_with_expression(
            lambda x: (x**3) * math.log(x, math.e), (1, 3, (3 - 1) / 4)
        )
    )


# %%
def result_I_Simpson_with_expression(
    expression: object,
    interval: tuple,
    weight: int = 10000,
) -> float:
    if not callable(expression):
        raise TypeError("Expression must be callable")
    start = interval[0] * weight
    end = interval[1] * weight
    step = interval[2] * weight
    # ensure start, end and step are integers (allow float values that are whole numbers)
    start = _ensure_int(start, "start")
    end = _ensure_int(end, "end")
    step = _ensure_int(step, "step")
    intervals = list(range(start, end + step, step))

    def new_value(acc, item):
        index, value = item
        multiplier = 2
        if index % 2:
            multiplier = 4
        elif not index or index + 1 == len(intervals):
            multiplier = 1
        return acc + expression(value / weight) * multiplier

    total = reduce(new_value, enumerate(intervals), 0)
    # include endpoints
    return I_Simpson(step / weight, total)


def result_I_Simpson_with_y_list(
    y_list: list,
    h: float,
) -> float:
    def new_value(acc, item):
        index, y = item
        multiplier = 2
        if index % 2:
            multiplier = 4
        elif not index or index + 1 == len(y_list):
            multiplier = 1
        return acc + y * multiplier

    total = reduce(new_value, enumerate(y_list), 0)
    # include endpoints
    return I_Simpson(h, total)


if __name__ == "__main__":
    print(
        4 * result_I_Simpson_with_expression(lambda x: (1 + (x**2)) ** -1, (0, 1, 0.25))
    )
    print(
        result_I_Simpson_with_expression(
            lambda x: x * (math.e ** (2 * x)) / ((1 + 2 * x) ** 2), (0, 3, 0.5)
        )
    )


# %%
@singledispatch
def sum_two_values(a, b):
    raise TypeError("Unsupported types")


@sum_two_values.register
def _(a: int, b: int):
    return a + b


@sum_two_values.register
def _(a: list, b: list):
    return sum(a) + sum(b)


@sum_two_values.register
def _(a: bool, b: bool):
    return a and b


@sum_two_values.register
def _(a: object, b: object):
    if not callable(a) or not callable(b):
        raise TypeError("Expression must be callable")
    return a() + b()


if __name__ == "__main__":
    print(sum_two_values(2, 3))  # 5
    print(sum_two_values([2, 3, 4], [1, 2, 3]))  # 15
    print(sum_two_values(False, True))  # False
    print(type(teste))

# %%
