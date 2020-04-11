import inspect

from corelib.mobject.mobject import Mobject


def check_validity_of_attr(mobject, attr):
    if not hasattr(mobject, "target"):
        raise Exception(
            f"ERROR: {mobject} has no attribute {attr}"
        )


def check_validity_of_method(method):
    if not inspect.ismethod(method):
        raise Exception(
            "Whoops, looks like you accidentally invoked "
            "the method you want to animate"
        )
    assert (isinstance(method.__self__, Mobject))
