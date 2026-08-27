from collections import deque

def windowed(iterable, n):
    if n < 1:
        raise ValueError("n must be >= 1")
    it = iter(iterable)
    window = deque(maxlen=n)
    for item in it:
        window.append(item)
        if len(window) == n:
            yield tuple(window)
