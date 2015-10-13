#!/usr/bin/env python
"""
A "constant" datatype

"""
class _const:

    class ConstError(TypeError): 
        pass

    def __setattr__(self, name, value):
        name = str(name)
        if self.__dict__.has_key(name):
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        """Attributes may not be deleted"""
        name = str(name)
        if self.__dict__.has_key(name):
            raise self.ConstError("Can't unbind const(%s)" % name)
        raise NameError(name)

const = _const()

#const.YES = True
#const.NO = False

