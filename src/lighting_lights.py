#!/usr/bin/env python

"""Superclass

    Handle the lights component of the lighting system.
    This is the base data for all sub-classed lighting data
    
    Each entry should contain enough information to allow functionality of various family of
    lighting controllers.  Insteon is the first type coded and UPB is to follow.
    
    The real work of controlling the devices is delegated to the modules for that family of devices.
"""

import lighting_tools
import pprint


Light_Data = {}


class LightingData(lighting_tools.CoreData):

    def __init__(self):
        super(LightingData, self).__init__()

    def __str__(self):
        l_str = super(LightingData, self).__str__()
        return l_str


class LightingAPI(lighting_tools.CoreAPI, LightingData):
    """
    """

    def load_all_lights(self, p_dict):
        for l_key, l_dict in p_dict.iteritems():
            l_light = self.load_light(l_dict)
            Light_Data[l_key] = l_light

    def load_light(self, p_dict):
        """Load the light information.
        """
        l_light = LightingData()
        # Common Data
        l_light.Active = p_dict.get('Active', 'False')
        l_light.Comment = p_dict.get('Comment', None)
        l_light.Coords = p_dict.get('Coords', None)
        l_light.Dimmable = p_dict.get('Dimmable', False)
        l_light.Family = p_dict.get('Family', None)
        l_light.Name = p_dict.get('Name', 'NoName')
        l_light.Room = p_dict.get('Room', None)
        l_light.Type = p_dict.get('Type', None)
        return l_light

    def dump_all_lights(self):
        #super(LightingAPI, self).dump_all_lights()
        print "***** All Lights ***** lighting_lights"
        for l_key, l_obj in Light_Data.iteritems():
            print "~~~Light: {0:}".format(l_key)
            print "     ", l_obj
            print
            pprint.pprint(vars(l_obj))
            print "--------------------"
        print

    def update_all_devices(self):
        assert 0, "update all devices must be subclassed."

    def update_all_statuses(self):
        assert 0, "dump all statuses must be subclassed."

### END
