import matplotlib.pyplot as plt
import numpy as np
import logging

from .util.gui import ZoomPan, _timeout

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

# https://stackoverflow.com/questions/9997869/interactive-plot-based-on-tkinter-and-matplotlib
# https://stackoverflow.com/questions/33262433/unable-to-update-tkinter-matplotlib-graph-with-buttons-and-custom-data

def image_point_registration(img, timeout=None):
    """
    Launches a window which can be clicked to add points.
    """
    fig, ax = plt.subplots()
    points= []
    def on_click(event):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            ax.scatter(x, y, marker="D", s=50, zorder=2)
            ax.figure.canvas.draw()
            points.append([x, y])
        else:
            print("Clicked ouside axes bounds but inside plot window")

    fig.canvas.callbacks.connect("button_press_event", on_click)

    zp = ZoomPan()
    scale = 1.1
    figZoom = zp.zoom_factory(ax, base_scale=scale)
    ax.imshow(img)
    if timeout is not None:
        _timeout(fig, timeout)
        fig.timer.start()
    plt.show()
    return ax, points

if __name__ == '__main__':
    from scipy import misc
    image_point_registration(misc.face(), timeout=10000)
