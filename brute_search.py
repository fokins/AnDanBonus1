import numpy as np


class BruteSearch:
    def __init__(self, points):
        self.points = points
        self.distance_count = 0

    def find_k_nearest(self, target, k):
        self.distance_count = len(self.points)

        result = sorted(((np.linalg.norm(point - target), point) for point in self.points), key=lambda x: x[0])[:k]

        return result, self.distance_count