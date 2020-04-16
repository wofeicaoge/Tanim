from tanim.utils.constants import OUT
from tanim.utils.constants import PI
from tanim.utils.constants import TAU
from tanim.utils.rate_functions import linear

from tanim.core.animation.animation import Animation
from tanim.core.animation.transform import Transform


class Rotating(Animation):
    CONFIG = {
        "axis": OUT,
        "radians": TAU,
        "run_time": 5,
        "rate_func": linear,
        "about_point": None,
        "about_edge": None,
    }

    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)
        self.mobject.rotate(
            alpha * self.radians,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )


class Rotate(Transform):
    CONFIG = {
        "about_point": None,
        "about_edge": None,
    }

    def __init__(self, mobject, angle=PI, axis=OUT, **kwargs):
        if "path_arc" not in kwargs:
            kwargs["path_arc"] = angle
        if "path_arc_axis" not in kwargs:
            kwargs["path_arc_axis"] = axis
        self.angle = angle
        self.axis = axis
        super().__init__(mobject, **kwargs)

    def create_target(self):
        target = self.mobject.copy()
        target.rotate(
            self.angle,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )
        return target
