from functools import wraps
from random import randint


def timer_decorator(text):
    """Wrap decorated function in text template"""

    def timer(func):
        """Print random int from 1 to 9"""

        @wraps(func)
        def wrapper_timer(*args):
            message = text.format(randint(1, 10))
            print(message)
            return func(*args)

        return wrapper_timer

    return timer
