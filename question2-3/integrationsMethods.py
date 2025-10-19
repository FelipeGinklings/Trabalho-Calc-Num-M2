# %%
import math
from functools import reduce


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
def func(x):
    return (math.exp(-(x**2))) / (math.cos(x) + 2)


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

    y = [expression(x / weight) for x in range(start + step, end, step)]
    y = list(map(lambda x: x * 2, y))
    # include endpoints
    y.insert(0, expression(start / weight))
    y.append(expression(end / weight))
    return I_trapezoid(step / weight, sum(y))


# Regra dos Trapézios resultado
def result_I_trapezoid_with_y_list(y_list: list, h: int) -> float:
    scaled_y_values = [value * 2 for value in y_list]
    # include endpoints
    scaled_y_values.append(y_list[0])
    scaled_y_values.append(y_list[-1])
    return I_trapezoid(h, sum(scaled_y_values))


if __name__ == "__main__":
    print(round(result_I_trapezoid_with_expression(func, (0, 1, 1 / 50)), 6))


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
    print(round(result_I_Simpson_with_expression(func, (0, 1, 1 / 100)), 6))
