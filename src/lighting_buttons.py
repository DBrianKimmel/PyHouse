#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""


Button_Data = {}


class ButtonData(object):

    def __init__(self, Name):
        self.Name = Name

    def __repr__(self):
        l_ret = "Lighting Button Name:{0:}, Family:{1:} ".format(self.Name, self.Family)
        return l_ret

class ButtonAPI(ButtonData):
    """
    """

    def load_button(self, p_dict):
        """Load the button.
        """
        print "$$ lighting.load_button ", p_dict.keys()
        Name = p_dict.get('Name', 'NoName')
        l_button = ButtonData(Name)
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

    def dump_all_buttonss(self):
        for l_key, l_obj in Button_Data.iteritems():
            pass

### END
