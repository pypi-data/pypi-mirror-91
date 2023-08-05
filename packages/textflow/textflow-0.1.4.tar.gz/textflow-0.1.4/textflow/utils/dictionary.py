""" Dictionary object that creates attribute accessible dictionary objects.

references:
    https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
"""


class Dictionary(dict):
    """ Dictionary: Attribute accessible dictionary objects.

    Example:
        m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Dictionary, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Dictionary, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Dictionary, self).__delitem__(key)
        del self.__dict__[key]
