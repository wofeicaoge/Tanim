import inspect

import numpy as np

from corelib.animation.transform import Transform
from corelib.mobject.mobject import Group, Mobject

from utils.constants import DEFAULT_POINTWISE_FUNCTION_RUN_TIME
from utils.constants import DEGREES


class ReplacementTransform(Transform):
    CONFIG = {
        "replace_mobject_with_target_in_scene": True,
    }


class ClockwiseTransform(Transform):
    CONFIG = {
        "path_arc": -np.pi
    }


class CounterclockwiseTransform(Transform):
    CONFIG = {
        "path_arc": np.pi
    }


class MoveToTarget(Transform):
    def __init__(self, mobject, **kwargs):
        assert hasattr(mobject, "target")
        super().__init__(mobject, mobject.target, **kwargs)


class ApplyMethod(Transform):
    def __init__(self, method, *args, **kwargs):
        """
        method is a method of Mobject, *args are arguments for
        that method.  Key word arguments should be passed in
        as the last arg, as a dict, since **kwargs is for
        configuration of the transform itslef

        Relies on the fact that mobject methods return the mobject
        """
        assert inspect.ismethod(method)
        self.method = method
        self.method_args = args
        super().__init__(method.__self__, **kwargs)

    def create_target(self):
        method = self.method
        # Make sure it's a list so that args.pop() works
        args = list(self.method_args)

        if len(args) > 0 and isinstance(args[-1], dict):
            method_kwargs = args.pop()
        else:
            method_kwargs = {}
        target = method.__self__.copy()
        method.__func__(target, *args, **method_kwargs)
        return target


class ApplyPointwiseFunction(ApplyMethod):
    CONFIG = {
        "run_time": DEFAULT_POINTWISE_FUNCTION_RUN_TIME
    }

    def __init__(self, function, mobject, **kwargs):
        super().__init__(mobject.apply_function, function, **kwargs)


class ApplyPointwiseFunctionToCenter(ApplyPointwiseFunction):
    def __init__(self, function, mobject, **kwargs):
        self.function = function
        super().__init__(mobject.move_to, **kwargs)

    def begin(self):
        self.method_args = [
            self.function(self.mobject.get_center())
        ]
        super().begin()


class FadeToColor(ApplyMethod):
    def __init__(self, mobject, color, **kwargs):
        super().__init__(mobject.set_color, color, **kwargs)


class ScaleInPlace(ApplyMethod):
    def __init__(self, mobject, scale_factor, **kwargs):
        super().__init__(mobject.scale, scale_factor, **kwargs)


class ShrinkToCenter(ScaleInPlace):
    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, 0, **kwargs)


class Restore(ApplyMethod):
    def __init__(self, mobject, **kwargs):
        super().__init__(mobject.restore, **kwargs)


class ApplyFunction(Transform):
    def __init__(self, function, mobject, **kwargs):
        self.function = function
        super().__init__(mobject, **kwargs)

    def create_target(self):
        target = self.function(self.mobject.copy())
        if not isinstance(target, Mobject):
            raise Exception("Functions passed to ApplyFunction must return object of type Mobject")
        return target


class ApplyMatrix(ApplyPointwiseFunction):
    def __init__(self, matrix, mobject, **kwargs):
        matrix = self.initialize_matrix(matrix)

        def func(p):
            return np.dot(p, matrix.T)

        super().__init__(func, mobject, **kwargs)

    @staticmethod
    def initialize_matrix(matrix):
        matrix = np.array(matrix)
        if matrix.shape == (2, 2):
            new_matrix = np.identity(3)
            new_matrix[:2, :2] = matrix
            matrix = new_matrix
        elif matrix.shape != (3, 3):
            raise Exception("Matrix has bad dimensions")
        return matrix


class ApplyComplexFunction(ApplyMethod):
    def __init__(self, function, mobject, **kwargs):
        self.function = function
        method = mobject.apply_complex_function
        super().__init__(method, function, **kwargs)

    def init_path_func(self):
        func1 = self.function(complex(1))
        self.path_arc = np.log(func1).imag
        super().init_path_func()


class CyclicReplace(Transform):
    CONFIG = {
        "path_arc": 90 * DEGREES,
    }

    def __init__(self, *mobjects, **kwargs):
        self.group = Group(*mobjects)
        super().__init__(self.group, **kwargs)

    def create_target(self):
        target = self.group.copy()
        cycled_targets = [target[-1], *target[:-1]]
        for m1, m2 in zip(cycled_targets, self.group):
            m1.move_to(m2)
        return target


class Swap(CyclicReplace):
    pass  # Renaming, more understandable for two entries
