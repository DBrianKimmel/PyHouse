#!/usr/bin/env python

"""Tools for use in all lighting component files.
"""


# Import system type stuff
import inspect
from inspect import getmembers
import pprint


class LightingTools(object):

    def getBool(self, p_dict, p_field, p_default = 'False'):
        """Get field and return a bool as the value of the field.
        """
        l_field = p_dict.get(p_field, p_default)
        if l_field == 'False':
            return False
        if l_field == 'True':
            return True
        return False

    def getInt(self, p_dict, p_field):
        """Get a field and return as an int.
        """
        l_field = p_dict.get(p_field, 0)
        try:
            l_field = int(l_field, 0)
        except:
            l_field = int(l_field)
        return l_field

    def getFloat(self, p_dict, p_field):
        """Get field as a number - floating point is ok.
        """
        try:
            l_field = float(p_dict.get(p_field, 0.0))
        except TypeError:
            l_field = 0.0
        return l_field

    def getText(self, p_dict, p_field):
        l_field = p_dict.get(p_field, '')
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


class CoreData(LightingTools):

    def __init__(self):
        self.Active = None
        self.Comment = None
        self.Coords = None
        self.Dimmable = None
        self.Key = 0
        self.Family = None
        self.Name = None
        self.Room = None
        self.Type = None

    def __str__(self):
        l_str = "Light:: Name:{0:}, Family:{1:}, Type:{2:}, Comment:{3:}, Room:{4:}, Coords:{5:}, Active:{6:}, Dimmable:{7:}, ".format(
                            self.get_name(), self.get_family(), self.get_type(), self.get_comment(),
                            self.get_room(), self.get_coords(),
                            self.get_active(), self.get_dimmable())
        return l_str

    def get_active(self):
        return self.__Active
    def set_active(self, value):
        self.__Active = value
    def get_comment(self):
        return self.__Comment
    def set_comment(self, value):
        self.__Comment = value
    def get_coords(self):
        return self.__Coords
    def set_coords(self, value):
        self.__Coords = value
    def get_dimmable(self):
        return self.__Dimmable
    def set_dimmable(self, value):
        self.__Dimmable = value
    def get_family(self):
        return self.__Family
    def set_family(self, value):
        self.__Family = value
    def get_key(self):
        return self.__Key
    def set_key(self, value):
        self.__Key = value
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

    Active = property(get_active, set_active, None, "Bool - Active device or not.")
    Comment = property(get_comment, set_comment, None, "A general comment about the device.")
    Coords = property(get_coords, set_coords, None, None)
    Dimmable = property(get_dimmable, set_dimmable, None, None)
    Family = property(get_family, set_family, None, "The Family - Insteon, UPB, X10, etc.")
    Key = property(get_key, set_key, None, "Number 1..x that will be the dict key for this device.")
    Name = property(get_name, set_name, None, "The Name of the device.")
    Room = property(get_room, set_room, None, "The room where the device is located.")
    Type = property(get_type, set_type, None, "The device Type - Light, Controller, Button, Scene, ...")


class CoreAPI(LightingTools):
    """
    """

    def load_core_device(self, p_dict, p_key = 0):
        """Load the device (light/button/controller/... information into a new CoreData object.
        
        @param p_dict: The dict of config items for this one device.
        @return: a CoreData object filled in
        """
        l_dev = CoreData()
        l_dev.Active = self.getBool(p_dict, 'Active', False)
        l_dev.Comment = self.getText(p_dict, 'Comment')
        l_dev.Coords = self.getText(p_dict, 'Coords')
        l_dev.Dimmable = self.getBool(p_dict, 'Dimmable')
        l_dev.Family = self.getText(p_dict, 'Family')
        l_dev.Key = p_key
        l_dev.Name = self.getText(p_dict, 'Name')
        l_dev.Room = self.getText(p_dict, 'Room')
        l_dev.Type = self.getText(p_dict, 'Type')
        #print " - lighting_tools CoreAPI load device - {0:}".format(l_dev.Name)
        return l_dev

    def dump_device(self, p_obj, p_type = '', p_name = ''):
        print "~~~ {0:}: {1:}".format(p_type, p_name)
        print "     ", p_obj
        print
        pprint.pprint(vars(p_obj))
        print "--------------------"

### END
