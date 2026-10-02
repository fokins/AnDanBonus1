import numpy as np
from matplotlib.animation import FuncAnimation
from PIL import Image, ImageSequence

class GifOverlay:
    def __init__(self, fig, filename):
        self.fig = fig
        self.filename = filename
        self.animation = None
        self.frames, self.duration = self._load_gif()

    def _load_gif(self):
        gif = Image.open(self.filename)

        frames = []
        durations = []

        for frame in ImageSequence.Iterator(gif):
            data = np.array(frame.convert("RGBA"), dtype=np.uint8)

            r = data[:, :, 0].astype(np.int16)
            g = data[:, :, 1].astype(np.int16)
            b = data[:, :, 2].astype(np.int16)

            green = (
                (g > 50) &
                (g - r > 10) &
                (g - b > 10) &
                (g > r * 0.6) &
                (g > b * 0.6)
            )

            data[green, 3] = 0

            frames.append(data)
            durations.append(
                frame.info.get(
                    "duration",
                    gif.info.get("duration", 50)
                )
            )

        duration = durations[0] if durations else 50

        return frames, duration

    def play(self):
        # лежит в (0, 0) растянута на все изображение
        overlay = self.fig.add_axes([0, 0, 1, 1], zorder=100)
        overlay.set_axis_off()
        overlay.patch.set_alpha(0)

        image = overlay.imshow(
            self.frames[0],
            aspect="auto",
            interpolation="bilinear"
        )

        def update(i):
            if i < len(self.frames):
                image.set_data(self.frames[i])
                image.set_visible(True)
            else:
                image.set_visible(False)

            return image,

        self.animation = FuncAnimation(
            self.fig,
            update,
            frames=len(self.frames) + 1,
            interval=self.duration,
            blit=True,
            repeat=False
        )

        return self.animation
