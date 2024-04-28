import datetime
from typing import Callable


def measure_time(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        print(f"Measured running time of {func.__name__}: {end - start}")
        return result

    return wrapper

