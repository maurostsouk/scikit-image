from .base import Plugin
from ..utils import ClearColormap


class OverlayPlugin(Plugin):
    """Plugin for ImageViewer that displays an overlay on top of main image.

    Attributes
    ----------
    overlay : array
        Overlay displayed on top of image. This overlay defaults to a color map
        with alpha values varying linearly from 0 to 1.
    """
    colors = {'red': (1, 0, 0),
              'yellow': (1, 1, 0),
              'green': (0, 1, 0),
              'cyan': (0, 1, 1)}

    def __init__(self, **kwargs):
        super(OverlayPlugin, self).__init__(**kwargs)
        self._overlay_plot = None
        self._overlay = None
        self.cmap = None
        self.color_names = self.colors.keys()

    def attach(self, image_viewer):
        super(OverlayPlugin, self).attach(image_viewer)
        #TODO: `color` doesn't update GUI widget when set manually.
        self.color = 0

    @property
    def overlay(self):
        return self._overlay

    @overlay.setter
    def overlay(self, image):
        self._overlay = image
        ax = self.image_viewer.ax
        if image is None:
            ax.images.remove(self._overlay_plot)
            self._overlay_plot = None
        elif self._overlay_plot is None:
            self._overlay_plot = ax.imshow(image, cmap=self.cmap)
        else:
            self._overlay_plot.set_array(image)
        self.image_viewer.redraw()

    def display_filtered_image(self, image):
        """Display image over image in viewer."""
        self.overlay = image

    def closeEvent(self, event):
        self.overlay = None
        super(OverlayPlugin, self).closeEvent(event)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, index):
        # Update colormap whenever color is changed.
        name = self.color_names[index]
        self._color = name
        rgb = self.colors[name]
        self.cmap = ClearColormap(rgb)

        if self._overlay_plot is not None:
            self._overlay_plot.set_cmap(self.cmap)
        self.image_viewer.redraw()
