#!/usr/bin/python

"""Load the database with X10 devices.
"""

# Import system type stuff
import logging

# Import PyMh files
from lighting import lighting

g_debug = 0


class X10LightingData(lighting.LightData):

    def __init__(self):
        lighting.LightData.__init__(self)
        self.set_family("X10")
        self.Address = 'asdf'


class LightingAPI(lighting.LightingAPI):
    """Overload the base methods with specific ones here.
    """

    def change_light_setting(self, p_obj, p_level):
        pass

    def update_all_lights(self):
        pass

    def turn_light_off(self, p_name):
        print "Turning off X10 light {0:}".format(p_name)

    def turn_light_on(self, p_name):
        print "Turning on X10 light {0:}".format(p_name)

    def turn_light_dim(self, p_name, p_level):
        print "Turning X10 light {0:} to level {1:}".format(p_name, p_level)

    def load_all_lights(self, p_dict):
        pass
        # lighting.LightingAPI.load_all_lights(self, p_dict)

    def scan_all_lights(self, p_lights):
        pass


class API(object):

    def __init__(self):
        """Constructor for the PLM.
        """
        if g_debug > 0:
            print "Device_X10.__init__()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.Device_X10')
        # LightingAPI().load_all_lights(Configure_Data['X10Lights'])
        g_logger.info('Initialized.')

    def Start(self, p_obj):
        if g_debug > 0:
            print "Device_X10.Start()"
        g_logger.info('Starting.')
        g_logger.info('Started.')

    def Stop(self):
        if g_debug > 0:
            print "Device_X10.Stop()"
        pass

# ## END
