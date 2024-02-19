import numpy as np

# Sum of the min & max of (a, b, c)
def hilo(a, b, c):
    if c < b:
        b, c = c, b
    if b < a:
        a, b = b, a
    if c < b:
        b, c = c, b
    return a + c


def complement(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))


def convert_incoming_color(r, g, b):
    r = int(1.1*int(r))
    g = int(1.1*int(g))
    b = int(1.1*int(b))
    return r, g, b


class LoopBuffer:
    def __init__(self, size, default_value=0):
        self.size = size
        self.buffer = [default_value] * size
        self.index = 0

    def append(self, value):
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size

    def max(self) -> float:
        return max(self.buffer)

    def min(self) -> float:
        return min(self.buffer)

    def average(self) -> float:
        return sum(self.buffer) / self.size

    def override_all(self, value):
        self.buffer = [value] * self.size

    def override_last(self, value):
        self.buffer[self.index] = value

    def variance(self) -> float:
        return np.var(self.buffer)

