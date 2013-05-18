#!/usr/bin/env python

"""Tools for use in all lighting component files.
"""


# Import system type stuff
# import inspect
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
        except TypeError:
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
    """Information
    """

    def __init__(self):
        self.Active = False
        self.Comment = ''
        self.Coords = ''
        self.Dimmable = False
        self.Driver = None
        self.Key = 0
        self.Family = ''
        self.Name = ''
        self.RoomName = ''
        self.Type = ''

    def __repr__(self):
        l_str = "Light:: "
        l_str += "Name:{0:}, ".format(self.Name)
        l_str += "Family:{0:}, ".format(self.Family)
        l_str += "Type:{0:}, ".format(self.Type)
        l_str += "Comment:{0:}, ".format(self.Comment)
        l_str += "Room:{0:}, ".format(self.RoomName)
        l_str += "Coords:{0:}, ".format(self.Coords)
        l_str += "Active:{0:}, ".format(self.Active)
        l_str += "Dimmable:{0:}".format(self.Dimmable)
        return l_str


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
        l_dev.RoomName = self.getText(p_dict, 'Room')
        l_dev.Type = self.getText(p_dict, 'Type')
        # print " - lighting_tools CoreAPI load device - {0:}".format(l_dev.Name)
        return l_dev

    def dump_device(self, p_obj, p_type = '', p_name = ''):
        print "~~~ {0:}: {1:}".format(p_type, p_name)
        print "     ", p_obj
        print
        pprint.pprint(vars(p_obj))
        print "--------------------"

# ## END
