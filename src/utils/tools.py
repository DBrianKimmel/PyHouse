#!/usr/bin/python

"""Various tools that can be imported.  Named differently for recognition.

"""

def PrintBytes(p_message):
    """Print all the bytes of a message as hex bytes.
    """
    l_len = len(p_message)
    l_message = ''
    if l_len == 0:
        l_message = "<NONE>"
    else:
        for l_x in range(l_len):
            try:
                l_message += " {0:#04x}".format(int(p_message[l_x]))
            except ValueError:
                try:
                    l_message += " {0:#04X}".format(ord(p_message[l_x]))
                except TypeError:  # Must be a string
                    l_message += " {0:} ".format(p_message[l_x])
    l_message += " <END>"
    return l_message


class Lister():

    def __repr__(self):
        return ("<Instance of {0:}, Address {1:}:\n{2:}>\n".format(self.__class__.__name__, id(self), self.attrnames()))

    def attrnames(self):
        l_ret = ''
        for attr in self.__dict__.keys():
            if attr[:2] == '__':
                l_ret = l_ret + "\tName: {0:}=<built-in>\n".format(attr)
            else:
                l_ret = l_ret + "\tName: {0:}={1:}\n".format(attr, self.__dict__ [attr])
        return l_ret

def get_light_object(p_house, name = None, key = None):
    """return the light object for a given house using the given value.

    @param p_house: is the house object that contains the lights
    @return: the Light object found or None.
    """
    l_lights = p_house.Lights
    if name != None:
        for l_obj in l_lights.itervalues():
            if l_obj.Name == name:
                return l_obj
    elif key != None:
        for l_obj in l_lights.itervalues():
            if l_obj.Key == key:
                return l_obj
        return None

# ## END DBK