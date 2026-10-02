import time

from kd_tree import KDTree
from brute_search import BruteSearch
from points_generator import PointsGenerator
from plot import SearchPlot


N = 100_000
K_NEAREST = 10
DIMENSIONS = range(1, 21)


def main():
    tree_counts = []

    for dimension in DIMENSIONS:
        points = PointsGenerator(N, dimension).generate()
        target = PointsGenerator(1, dimension).generate()[0]

        tree = KDTree(points)
        brute_search = BruteSearch(points)

        start = time.perf_counter()
        tree_result, tree_distance_count = tree.find_k_nearest(target, K_NEAREST)
        tree_time = time.perf_counter() - start

        start = time.perf_counter()
        brute_result, brute_distance_count = brute_search.find_k_nearest(target, K_NEAREST)
        brute_time = time.perf_counter() - start

        print(f"Dimensions: {dimension}")
        print(f"KDTree:      {tree_distance_count} distances, {tree_time:.6f} s")
        print(f"Brute search: {brute_distance_count} distances, {brute_time:.6f} s")
        print()

        tree_counts.append(tree_distance_count)


    SearchPlot(DIMENSIONS, tree_counts).show()

if __name__ == "__main__":
    main()