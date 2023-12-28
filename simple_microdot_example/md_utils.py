import matplotlib.pyplot as plt
import io
import base64


class FigManager:
    def __init__(self, fig=None, ax=None):
        self.fig = fig
        self.ax = ax

    def __enter__(self):
        if self.fig is None:
            self.fig = plt.figure()
        if self.ax is None:
            self.ax = self.fig.add_subplot(111)
        return self.fig, self.ax

    def __exit__(self, exc_type, exc_val, exc_tb):
        plt.close(self.fig)

    def __call__(self, *args, **kwargs):
        return self.__enter__()

def encode_figure(fig, ax, clear_axis=True):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    if clear_axis:
        ax.cla()
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    return f'<img src="data:image/png;base64,{encoded.decode("utf-8")}" />'