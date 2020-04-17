from tanim.core.animation.animation import Animation


class UpdateFromFunc(Animation):
    """
    update_function of the form func(mobject), presumably
    to be used when the state of one mobject is dependent
    on another simultaneously animated mobject
    """
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def __init__(self, mobject, update_function, **kwargs):
        self.update_function = update_function
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        self.update_function(self.mobject)
