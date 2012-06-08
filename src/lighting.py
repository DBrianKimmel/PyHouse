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

# Import PyMh files
import configure_mh
import lighting_buttons
import lighting_controllers
import lighting_lights
import lighting_scenes
import lighting_status

#from tools import Lister


# These globals in the lighting singleton hold the operating data loaded at startup.
#Light_Status = {}
Button_Data = lighting_buttons.Button_Data
Controller_Data = lighting_controllers.Controller_Data
Light_Data = lighting_lights.Light_Data
Light_Status = lighting_status.Light_Status
Scene_Data = lighting_scenes.Scene_Data
Configure_Data = configure_mh.Configure_Data
g_reactor = None
g_logger = None


Singletons = {}
m_config = None
m_logger = None
m_family_module = []

' *!* Modules and pointers to the modules'
FAMILIES_AVAILABLE = ['Insteon', 'UPB', 'X10']
INTERFACES_AVAILABLE = ['Serial', 'USB', 'Ethernet']

m_InsteonDevice = None
m_X10Device = None
m_UpbDevice = None


class ButtonData(lighting_buttons.ButtonData): pass

class ButtonAPI(lighting_buttons.ButtonAPI, ButtonData): pass


class ControllerData(lighting_controllers.ControllerData): pass

class ControllerAPI(lighting_controllers.ControllerAPI): pass


class LightingData(lighting_lights.LightingData): pass

class LightingAPI(lighting_lights.LightingAPI): pass


class LightingStatusData(lighting_status.LightingStatusData): pass

class LightingStatusAPI(lighting_status.LightingStatusAPI): pass


class SceneData(lighting_scenes.SceneData): pass

class SceneAPI(lighting_scenes.SceneAPI): pass


class LightingUtility(ButtonAPI, ControllerAPI, LightingAPI, LightingStatusAPI):
    """The routines in this class ALL need modifying when a new 'Family' is added.
    
    To add a family do the following:
        Add the family name (Capitalized) to FAMILIES_AVAILABLE above
        Add a module named Device_<Family>.py
        Add any other modules needed by the Device module.  A module to interface with the controller is recommended.
        
    If the family uses a different driver, add the driver and add to INTERFACES_AVAILABLE above.
    """

    def _load_all_lighting_families(self):
        """ *!* 
        Get all the config information for all types of lights and scenes.
        """
        for _l_ix, i_family in enumerate(FAMILIES_AVAILABLE):
            l_import = 'Device_' + i_family
            l_ptr = __import__(l_import)
            l_main_ptr = l_ptr.DeviceMain()
            m_family_module.append(l_main_ptr)

    def _dump_all_lighting_families(self):
        self.dump_all_buttons()
        self.dump_all_controllers()
        self.dump_all_lights()

    def _start_all_lighting_families(self, p_reactor):
        """ *!* 
        """
        g_logger.info("_start_all_lighting_families()")
        for l_ptr in m_family_module:
            l_ptr.start(p_reactor)

    def _stop_all_lighting_families(self):
        """ *!* 
        """
        g_logger.info("_stop_all_lighting_families()")
        for l_ptr in m_family_module:
            l_ptr.stop()

    def change_light_setting(self, p_name, p_level = 0, _p_family = None):
        """ *!* API
        Turn a light to a given level (0-100) off/dimmed/on.
        The schedule does not know what the family that controls the light.
        """
        g_logger.info("Turn Light {0:} to level {1:}.".format(p_name, p_level))
        for l_ptr in m_family_module:
            l_ptr.change_light_setting(p_name, p_level)

    def update_all_lighting_families(self):
        """ *!*  API
        Update the light configs in the appropriate module.
        """
        g_logger.info("update_all_lighting_families()")
        for l_ptr in m_family_module:
            l_ptr.update_all_lights()

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


def Init():
    global g_logger
    g_logger = logging.getLogger('PyHouse.Lighting')
    g_logger.info("Initializing")
    LightingUtility()._load_all_lighting_families()
    SceneAPI().load_all_scenes(configure_mh.Configure_Data['Scenes'])
    #self._dump_all_lighting_families()
    g_logger.info("Initialized.")
    pass

def start(p_reactor):
    """Allow loading of sub modules and drivers.
    """
    LightingUtility()._start_all_lighting_families(p_reactor)

def stop():
    """Allow cleanup of all drivers.
    """
    LightingUtility()._stop_all_lighting_families()

### END
