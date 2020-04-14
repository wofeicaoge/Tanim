from corelib.animation.movement import *
from extention.utils.rate_functions import linear


class Homotopy(Move):
    CONFIG = {
        "run_time": 3
    }

    def get_apply_function(self, t):
        return lambda p: self.function(*p, t)

    def interpolate_submobject(self, submob, start, alpha):
        submob.points = start.points
        super().interpolate_submobject(submob, start, alpha)


class SmoothedVectorizedHomotopy(Homotopy):
    def interpolate_submobject(self, submob, start, alpha):
        Homotopy.interpolate_submobject(self, submob, start, alpha)
        submob.make_smooth()


class ComplexHomotopy(Homotopy):
    def __init__(self, complex_homotopy, mobject, **kwargs):
        """
        Complex Hootopy a function Cx[0, 1] to C
        """

        def homotopy(x, y, z, t):
            c = complex_homotopy(complex(x, y), t)
            return c.real, c.imag, z

        Homotopy.__init__(self, homotopy, mobject, **kwargs)


class PhaseFlow(Move):
    CONFIG = {
        "virtual_time": 1,
        "rate_func": linear,
        "suspend_mobject_updating": False,
    }

    def get_apply_function(self, t):
        return lambda p: p + t * self.function(*p)

    def interpolate_mobject(self, alpha):
        if hasattr(self, "last_alpha"):
            dt = self.virtual_time * (alpha - self.last_alpha)
            super().interpolate_submobject(self.mobject, None, dt)
        self.last_alpha = alpha
