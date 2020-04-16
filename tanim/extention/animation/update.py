import operator as op

from tanim.core.animation.animation import Animation
from tanim.core.animation.update import UpdateFromFunc


class UpdateFromAlphaFunc(UpdateFromFunc):
    def interpolate_mobject(self, alpha):
        self.update_function(self.mobject, alpha)


class MaintainPositionRelativeTo(Animation):
    def __init__(self, mobject, tracked_mobject, **kwargs):
        self.tracked_mobject = tracked_mobject
        self.diff = op.sub(
            mobject.get_center(),
            tracked_mobject.get_center(),
        )
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        target = self.tracked_mobject.get_center()
        location = self.mobject.get_center()
        self.mobject.shift(target - location + self.diff)