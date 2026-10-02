import numpy as np

MAX_COORDINATE = 1000

class PointsGenerator:
    def __init__(self, n, k):
        self.n = n
        self.k = k

    def generate(self):
        return np.random.randint(-MAX_COORDINATE, MAX_COORDINATE + 1, size=(self.n, self.k))