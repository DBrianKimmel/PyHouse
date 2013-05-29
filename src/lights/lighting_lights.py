#!/usr/bin/env python

"""Handle the lights component of the lighting system.

    Each entry should contain enough information to allow functionality of various family of
    lighting controllers.  Insteon is the first type coded and UPB is to follow.

    The real work of controlling the devices is delegated to the modules for that family of devices.
"""

# Import PyHouse files
from src.lights import lighting_tools


g_debug = 0
# 0 = off


class LightData(lighting_tools.CoreData):

    def __init__(self):
        if g_debug >= 2:
            print "lighting_lights.LightsData.__init__()"
        super(LightData, self).__init__()
        self.Controller = None
        self.Type = 'Light'
        self.CurLevel = 0

    def __repr__(self):
        l_str = super(LightData, self).__repr__()
        l_str = l_str + " Key:{0} ".format(self.Key)
        return l_str

# ## END DBK
