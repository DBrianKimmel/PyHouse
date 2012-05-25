#!/usr/bin/env python

"""Tools for use in all lighting component files.
"""


# Import system type stuff
import inspect
from inspect import getmembers


class LightingTools(object):

    def __init__(self):
        self.Active = None
        self.Comment = None
        self.Family = None
        self.Name = None
        self.Room = None
        self.Type = None

    def get_active(self):
        return self.__Active
    def set_active(self, value):
        self.__Active = value
    def get_comment(self):
        return self.__Comment
    def set_comment(self, value):
        self.__Comment = value
    def get_family(self):
        return self.__Family
    def set_family(self, value):
        self.__Family = value
    def get_name(self):
        return self.__Name
    def set_name(self, value):
        self.__Name = value
    def get_room(self):
        return self.__Room
    def set_room(self, value):
        self.__Room = value
    def get_type(self):
        return self.__Type
    def set_type(self, value):
        self.__Type = value

    Active = property(get_active, set_active, None, "Active device or not - Bool")
    Comment = property(get_comment, set_comment, None, "A general comment about the device")
    Family = property(get_family, set_family, None, "The Family - Insteon, UPB, X10, etc.")
    Name = property(get_name, set_name, None, "The Name of the device")
    Room = property(get_room, set_room, None, "The room where the device is located")
    Type = property(get_type, set_type, None, "The device Type - Light, Controller, Button, Scene, ...")

    def getBool(self, p_dict, p_field):
        l_field = p_dict.get(p_field, 0)
        if l_field == 0:
            return False
        if l_field.lower() == 'true':
            return True
        return False

    def getInt(self, p_dict, p_field):
        l_field = p_dict.get(p_field, 0)
        try:
            l_field = int(l_field, 0)
        except:
            l_field = int(l_field)
        return l_field

    def getText(self, p_dict, p_field):
        l_field = p_dict.get(p_field, 0)
        return l_field

    def getValue(self, p_dict, p_field):
        """Return None if config value is 'None'
        """
        l_field = p_dict.get(p_field, None)
        if l_field == 'None': l_field = None
        return l_field

    def convert_to_dict(self, p_obj):
        l_dict = {}
        l_list = getmembers(p_obj)
        for l_pair in l_list:
            l_ix = l_list[0].find('__')
            if l_ix > 0:
                l_pair[0] = l_pair[0][(l_ix + 2):]
            l_dict[l_pair[0]] = l_pair[1]
        return l_dict

### END
