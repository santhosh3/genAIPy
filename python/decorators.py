import time


def time_in(func):
    running = False

    def wrapper(*args, **kwargs):
        nonlocal running
        if running:
            return func(*args, **kwargs)
        running = True
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        running = False
        print(f"time taken to execute {func.__name__}: {end - start:.6f} seconds")
        return result

    return wrapper


@time_in
def fib(n):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)


print(fib(40))