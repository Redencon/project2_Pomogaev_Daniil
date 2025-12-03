from functools import wraps
from time import monotonic

import prompt


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(e)
        except ValueError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
    return wrapper

def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*arfs, **kwargs):
            rep = prompt.string(
                f"Вы уверены, что хотите выполнить \"{action_name}\"? [y/n]: "
            )
            if rep == "y":
                return func(*arfs, **kwargs)
            else:
                print("Действие отменено")
        return wrapper
    return decorator


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = monotonic()
        result = func(*args, **kwargs)
        end_time = monotonic()
        print(
            f"Функция {func.__name__} выполнялась за {end_time - start_time:.3f} секунд"
        )
        return result
    return wrapper


def create_cacher():
    cache = {}
    def cache_result(key, value_func):
        if key not in cache:
            cache[key] = value_func()
        return cache[key]
    return cache_result