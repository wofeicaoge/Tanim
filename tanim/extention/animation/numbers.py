from tanim.utils.bezier import interpolate

from tanim.core.animation.animation import Animation

from tanim.extention.mobject.numbers import DecimalNumber


class ChangingDecimal(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def __init__(self, decimal_mob, number_update_func, **kwargs):
        assert isinstance(decimal_mob, DecimalNumber)
        self.number_update_func = number_update_func
        super().__init__(decimal_mob, **kwargs)

    def interpolate_mobject(self, alpha):
        self.mobject.set_value(
            self.number_update_func(alpha)
        )


class ChangeDecimalToValue(ChangingDecimal):
    def __init__(self, decimal_mob, target_number, **kwargs):
        start_number = decimal_mob.number
        super().__init__(
            decimal_mob,
            lambda a: interpolate(start_number, target_number, a),
            **kwargs
        )
