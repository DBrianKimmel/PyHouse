#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

import lighting_tools
import pprint

Button_Data = {}


class ButtonData(lighting_tools.LightingTools):

    def __init__(self):
        self.Type = 'Button'

    def __repr__(self):
        l_ret = "Lighting Button - Name:{0:}, Family:{1:}, Type:{2:} ".format(self.Name, self.Family, self.Type)
        return l_ret

class ButtonAPI(ButtonData):
    """
    """

    def load_all_buttons(self, p_dict):
        for l_key, l_dict in p_dict.iteritems():
            self.load_button(l_dict)

    def load_button(self, p_dict):
        """Load the button.
        """
        Name = p_dict.get('Name', 'NoName')
        l_button = ButtonData()
        # Common Data
        l_button.Active = p_dict.get('Active', 'False')
        l_button.Address = p_dict.get('Address', '01.23.45')
        l_button.Comment = p_dict.get('Comment', '')
        l_button.Coords = p_dict.get('Coords', (0, 0))
        l_button.Family = p_dict.get('Family', 'None')
        l_button.Name = Name
        l_button.Room = p_dict.get('Room', None)
        l_button.Type = p_dict.get('Type', None)
        # Insteon Data
        l_button.GroupList = p_dict.get('GroupList', '')
        l_button.GroupNumber = p_dict.get('GroupNumber', 0)
        l_button.Controller = p_dict.get('Controller', False)
        l_button.Responder = p_dict.get('Responder', False)
        l_button.Dimmable = p_dict.get('Dimmable', False)
        l_button.DevCat = p_dict.get('DevCat', 0)
        l_button.Master = p_dict.get('Master', True)
        l_button.Code = p_dict.get('Code', '')
        l_button.Responder = p_dict.get('Responder', False)
        # UPB Data
        #
        Button_Data[Name] = l_button
        return l_button

    def dump_all_buttons(self):
        print "***** All Buttons *****"
        for l_key, l_obj in Button_Data.iteritems():
            print "~~~Button: {0:}".format(l_key)
            print "     ", l_obj
            print
            pprint.pprint(vars(l_obj))
            print "--------------------"
        print

### END
