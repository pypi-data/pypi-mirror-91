SPECIAL_ATTRS = {"__class__", "__qualname__", "__module__", "__doc__", "__bases__"}


class ThingClass(type):
    def __getattr__(cls, attr):
        print('attr:', attr)
        attr = "__%s" % attr
        return cls.__dict__[attr]

    def __setattr__(cls, attr, value):
        if attr in SPECIAL_ATTRS:
            super().__setattr__(attr, value)
        else:
            attr = "__%s" % attr
            type.__setattr__(cls, attr, values)


class Atom(metaclass=ThingClass):
    pass


def get_preferred_label(cls):
    return "my preferred label"

def get_parents(cls):
    return "Adam & Eva"

# Works
#ThingClass.get_preferred_label = get_preferred_label
#ThingClass.get_parents = get_parents
setattr(ThingClass, 'get_preferred_label', get_preferred_label)
setattr(ThingClass, 'get_parents', get_parents)


print(Atom.get_preferred_label())
print(Atom.get_parents())
