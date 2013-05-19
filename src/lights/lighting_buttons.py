#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

# Import PyHouse files
from src.lights import lighting_tools

ButtonCount = 0


class ButtonsData(lighting_tools.CoreData):

    def __init__(self):
        global ButtonCount
        super(ButtonsData, self).__init__()
        ButtonCount += 1
        self.Type = 'Button'

    def __repr__(self):
        l_str = super(ButtonsData, self).__repr__()
        return l_str

class ButtonsAPI(lighting_tools.CoreAPI):
    """
    """

    def __init__(self):
        super(ButtonsAPI, self).__init__()

    def get_ButtonCount(self):
        return ButtonCount

    def load_button(self, p_dict, p_button):
        """Load the button.
        """
        l_button = super(ButtonsAPI, self).load_core_device(p_dict, self.get_ButtonCount())
        return l_button

# ## END DBK
