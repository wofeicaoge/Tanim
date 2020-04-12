from corelib.animation.animation import Animation


class Movement(Animation):
    CONFIG = {
        "apply_function_kwargs": {},
    }

    def __init__(self, function, mobject, **kwargs):
        self.function = function
        super().__init__(mobject, **kwargs)

    def get_apply_function(self, alpha):
        return self.function

    def interpolate_submobject(self, submob, start, alpha):
        submob.apply_function(
            self.get_apply_function(alpha),
            **self.apply_function_kwargs
        )


class MoveAlongPath(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def __init__(self, mobject, path, **kwargs):
        self.path = path
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        point = self.path.point_from_proportion(alpha)
        self.mobject.move_to(point)
