from corelib.animation.animation import Animation


class ShowCreation(Animation):
    CONFIG = {
        "lag_ratio": 1,
        "lower_bound": 0
    }

    def interpolate_submobject(self, submob, start_submob, alpha):
        submob.pointwise_become_partial(
            start_submob, *self.get_bounds(alpha)
        )

    def get_bounds(self, alpha):
        return self.lower_bound, alpha
