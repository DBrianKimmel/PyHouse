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
g_reactor = None


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
class ButtonAPI(lighting_buttons.ButtonAPI): pass

class ControllerData(lighting_controllers.ControllerData):
    def __init__(self):
        lighting_controllers.ControllerData.__init__(self)
class ControllerAPI(lighting_controllers.ControllerAPI):
    def load_all_controllers(self, p_dict):
        lighting_controllers.ControllerAPI.load_all_controllers(self, p_dict)

class LightingData(lighting_lights.LightingData): pass
class LightingAPI(lighting_lights.LightingAPI): pass

class LightingStatusData(lighting_status.LightingStatusData): pass
class LightingStatusAPI(lighting_status.LightingStatusAPI): pass

class SceneData(lighting_scenes.SceneData): pass
class SceneAPI(lighting_scenes.SceneAPI): pass

class LightingUtility(LightingAPI, LightingData):
    """The routines in this class ALL need modifying when a new 'Family' is added.
    """

    def load_all_lighting_families(self):
        """Get all the config information for all types of lights and scenes.
        
        # *!* 
        """
        self.m_logger.info("load_all_lighting_families()")
        cfg_dict = self.m_config.get_value()
        for l_ix, i_family in enumerate(FAMILIES_AVAILABLE):
            l_import = 'Device_' + i_family
            l_ptr = __import__(l_import)
            l_main_ptr = l_ptr.DeviceMain()
            m_family_module.append(l_main_ptr)

    def start_all_lighting_families(self):
        """ *!* 
        """
        self.m_logger.info("start_all_lighting_families()")
        for l_ptr in m_family_module:
            l_ptr.start(self.m_reactor)

    def stop_all_lighting_families(self):
        for l_ptr in m_family_module:
            l_ptr.stop()

    def change_light_setting(self, p_name, p_level = 0, _p_family = None):
        """ *!* 
        Turn a light to a given level (0-100) off/dimmed/on.
        """
        #self.m_logger.info("change_light_setting()")
        #self.m_logger.info("Turn Light {0:} to level {1:}.".format(p_name, p_level))
        for l_ptr in m_family_module:
            l_ptr.change_light_setting(p_name, p_level)

    def update_all_lighting_families(self):
        self.m_logger.info("update_all_lighting_families()")
        for l_ptr in m_family_module:
            l_ptr.update_all_lights()

    def update_all_light_tables(self, p_lights):
        """ *!* 
        Get an updated lighting table from a module (say web server).
        Call each of the loaded family type classes to store its particular information.
        Load updated tables back into the config files.
        
        @param p_lights: is the entire lighting table (from web server and perhaps others)
        """

        if self.m_InsteonDevice != None:
            self.m_InsteonDevice.update_all_lights()
        if self.m_UpbDevice != None:
            self.m_UpbDevice.update_all_lights()
        if self.m_X10Device != None:
            self.m_X10Device.update_all_lights()

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


class SceneUtility(SceneAPI):

    def load_scene_data(self):
        self.m_logger.info("Using Scenes.")
        l_dict = self.m_config.get_value('Scenes')
        for l_key, l_value in l_dict.iteritems():
            self.Scene_Data[l_key] = {}
            for l_par, l_var in l_value.iteritems():
                self.Scene_Data[l_key][l_par] = l_var
        return self.Scene_Data


class LightingMain(LightingUtility, SceneUtility, LightingAPI, ControllerAPI, ButtonAPI):
    """Main interface to lighting for the home.
    
    Create a singleton since this will be called from many different places/
    """

    def __new__(cls, *args, **kwargs):
        """Create a singleton.
        Initialize the 1st time only - after that just return the single instance
        """
        if cls in Singletons:
            return Singletons[cls]
        self = object.__new__(cls)
        cls.__init__(self, *args, **kwargs)
        Singletons[cls] = self
        self.m_logger = logging.getLogger('PyHouse.Lighting')
        self.m_config = configure_mh.ConfigureMain()
        self.load_all_lighting_families()
        self.load_all_scenes(self.m_config.get_value('Scenes'))
        self.m_logger.info("Initialized.")
        return self

    def __init__(self):
        """Constructor for the component
        """

    def start(self, p_reactor):
        self.m_reactor = p_reactor
        self.start_all_lighting_families()

    def stop(self):
        pass

### END
