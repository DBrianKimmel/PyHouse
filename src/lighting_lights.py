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


class LightingData(lighting_tools.CoreData):

    #LightCount = 0

    def __init__(self):
        global LightCount
        #print " L lighting_lights LightingData init"
        super(LightingData, self).__init__()
        LightCount += 1
        self.Type = 'Light'

    def __str__(self):
        l_str = super(LightingData, self).__str__()
        l_str = l_str + " Key:{0} ".format(self.get_key())
        return l_str

class LightingAPI(lighting_tools.CoreAPI):

    def __init__(self):
        #print " L lightingAPI.__init__()"
        super(LightingAPI, self).__init__()

    def get_LightCount(self):
        global LightCount
        #print " L LightCount = ", LightCount
        return LightCount

    def load_light(self, p_dict, p_light):
        """Load the light information.
        """
        #print " L load_light() - {0:}".format(p_light.Name)
        l_light = super(LightingAPI, self).load_core_device(p_dict, self.get_LightCount())
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

### END
