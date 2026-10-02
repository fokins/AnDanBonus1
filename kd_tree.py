import heapq
import numpy as np
from node import Node


class KDTree:
    def __init__(self, points):
        self.dimension = points.shape[1]
        self.root = self._build_recursive(points, 0)
        self.distance_count = 0

    def _build_recursive(self, points, cur_depth):
        if len(points) == 0:
            return None

        cur_axis = cur_depth % self.dimension
        median = len(points) // 2

        # np.argpartition - возвращает массив в таком порядке, чтобы median был на своем места,
        # все элементы левее были меньше, а все элементы справа больше
        # работает за ~ O(n)
        points = points[np.argpartition(points[:, cur_axis], median)]

        node = Node(points[median], cur_axis)

        node.left = self._build_recursive(points[:median], cur_depth + 1)
        node.right = self._build_recursive(points[median + 1:], cur_depth + 1)

        return node

    def find_k_nearest(self, target, k):
        heap = []
        self.distance_count = 0
        self._search_k_recursive(self.root, target, k, heap)

        result = []
        for elem in heap:
            result.append((elem[0], elem[2]))

        return result.sort(key=lambda x: x[0]), self.distance_count

    def _search_k_recursive(self, node, target, k, heap):
        if node is None:
            return

        distance = np.linalg.norm(node.point - target)
        self.distance_count += 1

        # self.distance_count - чтобы при равном расстоянии сравнивать по номеру, а не по массиву
        cur_elem = (distance, self.distance_count, node.point)

        if len(heap) < k:
            heapq.heappush_max(heap, cur_elem)
        elif distance < heap[0][0]:
            heapq.heapreplace_max(heap, cur_elem)

        cur_axis = node.axis
        cur_coordinate_difference = target[cur_axis] - node.point[cur_axis]

        if cur_coordinate_difference < 0:
            closest_part = node.left
            farest_part = node.right
        else:
            closest_part = node.right
            farest_part = node.left

        self._search_k_recursive(closest_part, target, k, heap)

        if len(heap) < k or abs(cur_coordinate_difference) < heap[0][0]:
            self._search_k_recursive(farest_part, target, k, heap)