#!/usr/bin/env python

"""Superclass

    Handle the lights component of the lighting system.
    This is the base data for all sub-classed lighting data

    Each entry should contain enough information to allow functionality of various family of
    lighting controllers.  Insteon is the first type coded and UPB is to follow.

    The real work of controlling the devices is delegated to the modules for that family of devices.
"""

import lighting_tools

Light_Data = {}
LightCount = 0
g_debug = 1


class LightData(lighting_tools.CoreData):

    def __init__(self):
        global LightCount
        LightCount += 1
        if g_debug > 1:
            print "lighting_lights.LightsData.__init__()"
        super(LightData, self).__init__()
        self.Type = 'Light'
        self.CurLevel = 0

    def __str__(self):
        l_str = super(LightData, self).__str__()
        l_str = l_str + " Key:{0} ".format(self.get_key())
        return l_str

    def get_cur_level(self):
        return self.__CurLevel
    def set_cur_level(self, value):
        self.__CurLevel = value

    CurLevel = property(get_cur_level, set_cur_level, None, "Device light level - 0=Off, 100=Full On")


class LightsAPI(lighting_tools.CoreAPI):

    def __init__(self):
        if g_debug > 1:
            print "lighting_lights.lightsAPI.__init__()"
        super(LightsAPI, self).__init__()

    def _get_LightCount(self):
        global LightCount
        return LightCount

    def load_light(self, p_dict, p_light):
        """Load the light information.
        """
        if g_debug > 1:
            print "lighting_lights.LightsAPI.load_light() - {0:}".format(p_light.Name)
        l_light = super(LightsAPI, self).load_core_device(p_dict, self._get_LightCount())
        l_light.CurLevel = 0
        return l_light

    def dump_all_lights(self):
        print "***** All Lights ***** lighting_lights"
        for l_key, l_obj in Light_Data.iteritems():
            self.dump_device(l_obj, 'Light', l_key)
        print

    def update_all_devices(self):
        assert 0, "update all devices must be subclassed."

    def update_all_statuses(self):
        assert 0, "dump all statuses must be subclassed."

# ## END
