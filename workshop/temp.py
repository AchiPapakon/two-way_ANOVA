class BaseClass(object):
    def __init__(self, mark=None, name=None):   # you're using named parameters, declare them as named one.
        self.mark = mark
        self.name = name


class DerivedClass(BaseClass):   # don't forget to declare inheritance
    def __init__(self, *args, rank, **kwargs):    # in args, kwargs, there will be all parameters you don't care, but needed for baseClass
        super(DerivedClass, self).__init__(*args, **kwargs)
        self.rank = rank

b1 = DerivedClass(rank='Jibin')
print(b1.rank)