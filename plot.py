import matplotlib.pyplot as plt
import numpy as np

from gif_overlay import GifOverlay


class SearchPlot:
    def __init__(self, dimensions, tree_counts):
        self.dimensions = dimensions
        self.tree_counts = tree_counts
        self.overlay = None

    def show(self):
        x = np.arange(len(self.dimensions))

        fig, ax = plt.subplots()

        ax.bar(x, self.tree_counts, width=0.8, color="skyblue")

        ax.set_xlabel("Dimension")
        ax.set_ylabel("Distance calculations")
        ax.set_xticks(x, self.dimensions)
        ax.set_yscale("log")

        plt.tight_layout()

        self.overlay = GifOverlay(fig, "explosion.gif")
        self.overlay.play()

        plt.show()