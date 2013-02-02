#!/usr/bin/env python

"""Handle the home lighting system automation.

There are a number of lighting 'Family' types handled here.
The Insteon family is now functional.
The UPB family is work in progress
The X-10 family is mostly just a stub at present (2012)
New lighting families are added to this module.

Each family consists of four major areas:
    Lights / Lighting Devices
    Controllers - connected to the computer
    Scenes - have one or more lights that are controlled together
    Buttons - extra buttons with no light directly attached (key-pad-link)

This is a Main Module - always present.

    *!* - These are the places to add new lighting family information
"""

# Import system type stuff
import logging
import importlib

# Import PyMh files
import lighting_buttons
import lighting_controllers
import lighting_lights
import lighting_scenes
import lighting_status

g_debug = 0

g_reactor = None
g_logger = None
g_family_module = []
g_Device_family = []

FamilyCount = 0
Family_Data = {}

# These globals in the lighting singleton hold the operating data loaded at startup.
Light_Data = lighting_lights.Light_Data
Singletons = {}

' *!* Modules and pointers to the modules'
from families import VALID_FAMILIES
VALID_INTERFACES = ['Serial', 'USB', 'Ethernet']

m_InsteonDevice = None
m_X10Device = None
m_UpbDevice = None

class FamilyData(object):

    def __init__(self):
        global ScheduleCount
        self.Active = False
        self.Family = None
        self.Import = None
        self.Key = 0
        self.Name = None
        self.Package = None


class ButtonData(lighting_buttons.ButtonsData): pass

class ButtonAPI(lighting_buttons.ButtonsAPI): pass


class ControllerData(lighting_controllers.ControllerData): pass

class ControllerAPI(lighting_controllers.ControllersAPI): pass


class LightData(lighting_lights.LightData):

    def __init__(self):
        super(LightData, self).__init__()

    def __str__(self):
        return super(LightData, self).__str__()


class LightingAPI(lighting_lights.LightsAPI): pass


class LightingStatusData(lighting_status.LightingStatusData): pass

class LightingStatusAPI(lighting_status.LightingStatusAPI): pass


class SceneData(lighting_scenes.ScenesData): pass

class SceneAPI(lighting_scenes.ScenesAPI): pass


class LightingUtility(ButtonAPI, ControllerAPI, LightingAPI, LightingStatusAPI):
    """
    """

    m_module = []

    def load_lighting_families(self):
        """
        Get all the config information for all types of lights and scenes.
        """
        if g_debug > 1:
            print "lighting.load_lighting_families()"
        g_logger.info("Loading all lighting families.")
        for l_family in VALID_FAMILIES:
            l_family_obj = FamilyData()
            l_family_obj.Name = l_family
            l_family_obj.Package = 'families.' + l_family
            l_family_obj.Import = 'Device_' + l_family
            if g_debug > 1:
                print "lighting.load_all_lighting_families - Package: {0:}, Import: {1:}".format(l_family_obj.Package, l_family_obj.Import)
                print "  from {0:} import {1:}".format(l_family_obj.Package, l_family_obj.Import)
            l_module = importlib.import_module(l_family_obj.Package + '.' + l_family_obj.Import, l_family_obj.Package)
            g_family_module.append(l_module)
            g_Device_family.append(l_family_obj.Import)
            l_api = l_module.API()
            self.m_module.append(l_api)
            if g_debug > 1:
                print "lighting.load_lighting_families() - Added {0:} to m_modules".format(l_family_obj.Import), l_family_obj


    def start_lighting_families(self, p_obj):
        if g_debug > 1:
            print "lighting.start_lighting_families()", p_obj
        g_logger.info("Starting lighting families.")
        for l_mod in self.m_module:
            l_mod.Start(p_obj)

    def stop_lighting_families(self):
        if g_debug > 1:
            print "lighting.stop_lighting_families()"
        for l_mod in self.m_module:
            l_mod.Stop()

    def change_light_setting(self, p_obj, p_key, p_level):
        """
        Turn a light to a given level (0-100) off/dimmed/on.

        @param p_obj: is a house object
        @param p_key: is the index (Key) of the Light to be changed within the House object.
        @param p_level: is the level to set
        """
        if g_debug > 1:
            print "lighting.change_light_settings() House={0:}, Light={1:}({2:}), Level={3:}".format(p_obj.Name, p_obj.Lights[p_key].Name, p_key, p_level)
        g_logger.info("Turn Light {0:} to level {1:}.".format(p_obj.Lights[p_key].Name, p_level))
        for l_module in g_family_module:
            if g_debug > 1:
                print " Processing Module ", l_module
            l_module.LightingAPI().change_light_setting(p_obj.Lights[p_key], p_level)

    def update_all_lighting_families(self):
        """ *!*  API
        Update the light configs in the appropriate module.
        """
        g_logger.info("Updating all lighting families.")
        for l_module in g_family_module:
            l_module.LightingAPI().update_all_lights()

    def scan_all_lighting(self, p_lights):
        """ *!*
        """
        return
        if self.m_InsteonDevice != None:
            self.m_InsteonDevice.scan_all_lights(p_lights)
        if self.m_UpbDevice != None:
            self.m_UpbDevice.scan_all_lights(p_lights)
        if self.m_X10Device != None:
            self.m_X10Device.scan_all_lights(p_lights)

    def get_light_ref(self, p_house, p_light):
        """Return a light object reference for the given light in a house.
        """
        for l_obj in Light_Data.itervalues():
            print "get_light_ref()", l_obj.HouseName, l_obj.Name
            if l_obj.HouseName == p_house and l_obj.Name == p_light:
                return l_obj
        return None

def GetLightRef(p_house, p_light):
    """Return a light object reference for the given light in a house.
    """
    for l_obj in Light_Data.itervalues():
        if l_obj.HouseName == p_house and l_obj.Name == p_light:
            return l_obj
    return None


class API(LightingUtility):

    def __init__(self):
        if g_debug > 0:
            print "lighting.__init__()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.Lighting')
        g_logger.info("Initialized.")

    def Start(self, p_obj):
        """Allow loading of sub modules and drivers.
        """
        if g_debug > 0:
            print "lighting.Start() - House:{0:}".format(p_obj.Name)
        g_logger.info("Starting.")
        self.load_lighting_families()
        self.start_lighting_families(p_obj)
        g_logger.info("Started.")

    def Stop(self):
        """Allow cleanup of all drivers.
        """
        if g_debug > 0:
            print "lighting.Stop()"
        g_logger.info("Stopping all lighting families.")
        LightingUtility().stop_lighting_families()
        g_logger.info("Stopped.")

# ## END
