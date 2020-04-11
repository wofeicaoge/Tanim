from corelib.utils.config_ops import digest_config
from corelib.utils.iterables import list_update


# Currently, this is only used by both Scene and Mobject.
# Still, we abstract its functionality here, albeit purely nominally.
# All actual implementation has to be handled by derived classes for now.

# TODO: Move the "remove" functionality of Scene to this class


class Container(object):
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        self.submobjects = []  # Is it really better to name it submobjects?

    def add(self, *mobjects):
        if self in mobjects:
            raise Exception("Mobject cannot contain self")
        self.submobjects = list_update(self.submobjects, mobjects)
        return self

    def add_to_back(self, *mobjects):
        self.remove(*mobjects)
        self.submobjects = list(mobjects) + self.submobjects
        return self

    def remove(self, *mobjects, ):
        for mobject in mobjects:
            for submod in self.submobjects:
                if isinstance(submod, GroupContainer):
                    submod.remove(mobject)
                elif mobject == submod:
                    self.submobjects.remove(mobject)
        return self


class GroupContainer(Container):
    def __init__(self, *containers, **kwargs):
        self.add(*containers)
