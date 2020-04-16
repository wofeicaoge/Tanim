from tanim.extention.mobject.numbers import Integer
from tanim.core.mobject.vectorized_mobject import VGroup
from tanim.utils.color import Color


def print_family(mobject, n_tabs=0):
    """For debugging purposes"""
    print("\t" * n_tabs, mobject, id(mobject))
    for submob in mobject.submobjects:
        print_family(submob, n_tabs + 1)


def get_submobject_index_labels(mobject, label_height=0.15):
    labels = VGroup()
    for n, submob in enumerate(mobject):
        label = Integer(n)
        label.set_height(label_height)
        label.move_to(submob)
        label.set_stroke(Color('BLACK'), 5, background=True)
        labels.add(label)
    return labels