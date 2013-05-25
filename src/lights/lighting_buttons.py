#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

# Import PyHouse files
from src.lights import lighting_tools


class ButtonsData(lighting_tools.CoreData):

    def __init__(self):
        super(ButtonsData, self).__init__()
        self.Type = 'Button'

    def __repr__(self):
        l_str = super(ButtonsData, self).__repr__()
        return l_str

class ButtonsAPI(lighting_tools.CoreAPI):
    """
    """

    def __init__(self):
        super(ButtonsAPI, self).__init__()

# ## END DBK
