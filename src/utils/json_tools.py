'''
Created on Nov 6, 2013

@author: briank
'''

class JsonDict(dict):
    """A dictionary with attribute-style access. It maps attribute access to the real dictionary.
    """
    def __init__(self, init = {}):
        dict.__init__(self, init)

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(JsonDict, self).__setitem__(key, value)

    def __getitem__(self, name):
        item = super(JsonDict, self).__getitem__(name)
        return JsonDict(item) if type(item) == dict else item

    def __delitem__(self, name):
        return super(JsonDict, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        ch = JsonDict(self)
        return ch

# ## END DBK
