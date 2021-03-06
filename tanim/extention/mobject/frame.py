from tanim.utils.color import Color

from tanim.utils.config_ops import digest_config

from tanim.extention.mobject.geometry import Rectangle
import tanim.utils.constants as consts


class ScreenRectangle(Rectangle):
    CONFIG = {
        "aspect_ratio": 16.0 / 9.0,
        "height": 4
    }

    def __init__(self, **kwargs):
        Rectangle.__init__(self, **kwargs)
        self.set_width(
            self.aspect_ratio * self.get_height(),
            stretch=True
        )


class FullScreenRectangle(ScreenRectangle):
    CONFIG = {
        "height": consts.FRAME_HEIGHT,
    }


class FullScreenFadeRectangle(FullScreenRectangle):
    CONFIG = {
        "stroke_width": 0,
        "fill_color": Color('BLACK'),
        "fill_opacity": 0.7,
    }


class PictureInPictureFrame(Rectangle):
    CONFIG = {
        "height": 3,
        "aspect_ratio": 16.0 / 9.0
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        Rectangle.__init__(
            self,
            width=self.aspect_ratio * self.height,
            height=self.height,
            **kwargs
        )
