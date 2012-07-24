#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

import lighting_tools
import pprint

Button_Data = {}
ButtonCount = 0


class ButtonsData(lighting_tools.CoreData):

    def __init__(self):
        global ButtonCount
        #print " B lighting_buttons ButtonData init"
        super(ButtonsData, self).__init__()
        ButtonCount += 1
        self.Type = 'Button'

    def __str__(self):
        l_str = super(ButtonsData, self).__str__()
        return l_str

class ButtonsAPI(lighting_tools.CoreAPI):
    """
    """

    def __init__(self):
        #print " B lighting_buttons.__init__()"
        super(ButtonsAPI, self).__init__()

    def get_ButtonCount(self):
        return ButtonCount

    def load_button(self, p_dict, p_button):
        """Load the button.
        """
        l_button = super(ButtonsAPI, self).load_core_device(p_dict, self.get_ButtonCount())
        #print " B lighting_buttons.load_button() - {0:}".format(p_button.Name)
        #l_button.Address = p_dict.get('Address', '01.23.45')
        #l_button.GroupList = p_dict.get('GroupList', '')
        #l_button.GroupNumber = p_dict.get('GroupNumber', 0)
        #l_button.Controller = p_dict.get('Controller', False)
        #l_button.Responder = p_dict.get('Responder', False)
        #l_button.DevCat = p_dict.get('DevCat', 0)
        #l_button.Master = p_dict.get('Master', True)
        #l_button.Code = p_dict.get('Code', '')
        #l_button.Responder = p_dict.get('Responder', False)
        #Button_Data[l_button.Key] = l_button
        return l_button

    def dump_all_buttons(self):
        print "***** All Buttons *****"
        for l_key, l_obj in Button_Data.iteritems():
            self.dump_device(l_obj, 'Button', l_key)
        print

### END
