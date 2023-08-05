import functools
import time


def stdout_separated(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        print("------------------------------------------")
        return f(*args, **kwargs)

    return wrapper


def stdout_scan_time(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print(f"**** Port scanning took: {int(time.time() - start)} seconds.")
        return result

    return wrapper
