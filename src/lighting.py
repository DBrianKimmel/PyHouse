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

#from tools import Lister


# These globals in the lighting singleton hold the operating data loaded at startup.
Light_Data = {}
Light_Status = {}
Scene_Data = {}
Controller_Data = {}
Button_Data = {}


Singletons = {}
m_config = None
m_logger = None


' *!* pointers to the modules'
m_InsteonDevice = None
m_X10Device = None
m_UpbDevice = None


class LightingData(object):
    """Static data we wish to export/share.
    
    This is the base data for all sub-classed lighting data
    
    Each entry should contain enough information to allow functionality of various family of
    lighting controllers.  Insteon is the first type coded and UPB is to follow.
    
    The real work of controlling the devices is delegated to the modules for that family of devices.
    
    Standard characteristics for each light / switch button:
    """

    Name = 'NoName'
    Family = None
    Address = 'varies'
    Type = 'Undefined'
    Comment = 'Empty Comment'
    Controller = False
    Responder = False
    Dimmable = False
    Room = None
    Coords = 0, 0
    Master = False

    def __init__(self, Name):
        self.Name = Name

    def __repr__(self):
        l_str = "Lighting Name:{0:20.20s} Family: {1:10.10s} Type: {2:10.10s} Comment: {3:40.40s} Room: {4:} Coords: {5:}".format(
                            self.Family, self.Name, self.Type, self.Comment, self.Room, self.Coords)
        return l_str

    def get_Name(self):
        return self.Name

    def get_Type(self):
        return self.Type

    def get_Family(self):
        return self.Family

    def get_Comment(self):
        return self.Comment

    def get_Room(self):
        return self.Room

    def get_Coords(self):
        return self.Coords


class LightingStatus(object):
    """
    """
    CurLevel = 0

    def __init__(self, CurLevel):
        self.CurLevel = CurLevel

    def get_CurLevel(self):
        return self.CurLevel


class LightingAPI(LightingData):
    """A standardized dispatcher to control the lights.
    The actual work is passed to a family specific module.
    """

    def turn_light_off(self, _p_name):
        assert 0, "Turn light off must be subclassed."

    def turn_light_on(self, _p_name):
        assert 0, "Turn light on must be subclassed."

    def turn_light_dim(self, _p_name, _p_level):
        assert 0, "Turn light dim must be subclassed."

    def load_all_devices(self):
        assert 0, "Load all devices must be subclassed."

    def dump_all_devices(self):
        assert 0, "dump all devices must be subclassed."

    def update_all_devices(self):
        assert 0, "update all devices must be subclassed."

    def update_all_statuses(self):
        assert 0, "dump all statuses must be subclassed."


class SceneData(object):
    """
    """


class SceneAPI(SceneData):
    """
    """


class ControllerData(object):
    """
    """

    def __init__(self, Name):
        #print " --lighting.Controller_Data.__init__() ", Name
        self.Name = Name

    def X__repr__(self):
        l_ret = "Lighting Controller Name:{0:}, Family:{1:} ".format(self.Name, self.Family)
        return l_ret

    def get_Port(self):
        return self.Port

    def get_BaudRate(self):
        return int(self.BaudRate)

    def get_Family(self):
        return self.Family

    def get_Interface(self):
        return self.Interface


class ControllerAPI(ControllerData):
    """
    """

    def load_controllers(self, p_dict):
        """Load the common part of the controller.
        """
        #print " - Lighting.load_controllers ", p_dict.keys()
        Name = p_dict.get('Name', 'LightingController')
        l_ctlr = self.ControllerData(Name)
        l_ctlr.Family = p_dict.get('Family', 'Insteon')
        l_ctlr.Interface = p_dict.get('Interface', 'serial')
        l_ctlr.Port = p_dict.get('Port', '/dev/ttyUSB0')
        return l_ctlr

    def dump_all_controllers(self):
        pass


class ButtonData(object):

    def __init__(self, Name):
        self.Name = Name


class ButtonAPI(ButtonData):
    """
    """


class LightingUtility(LightingAPI):
    """The routines in this class mostly need modifying when a new 'Family' is added.
    """

    def clear_lighting_data(self):
        print " lighting.clear_lighting_data"
        #Light_Data = {}
        assert 0, 'FIX ME'

    def load_all_light_tables(self):
        """Get all the config information for all types of lights and scenes.
        
        # *!* 
        """
        #print " - Lighting.load_all_tables"
        self.m_logger.info("Loading All modules Lighting objects.")
        cfg_dict = self.m_config.get_value()
        if 'InsteonLights' in cfg_dict:
            import Device_Insteon
            self.m_InsteonDevice = Device_Insteon.InsteonDeviceMain()
        if 'UPBLights' in cfg_dict:
            import Device_UPB
            self.m_UpbDevice = Device_UPB.UPBDeviceMain()
        if 'X10Lights' in cfg_dict:
            import Device_X10
            self.m_X10Device = Device_X10.X10DeviceMain()

    def startup_all_lighting_modules(self):
        """ *!* 
        """
        if self.m_InsteonDevice != None:
            self.m_InsteonDevice.Insteon_startup()
        if self.m_UpbDevice != None:
            self.m_UpbDevice.start()
        if self.m_X10Device != None:
            self.m_X10Device.start()

    def update_all_light_tables(self, p_lights):
        """ *!* 
        Get an updated lighting table from a module (say web server).
        Call each of the loaded family type classes to store its particular information.
        Load updated tables back into the config files.
        
        @param p_lights: is the entire lighting table (from web server and perhaps others)
        """
        print "lighting.Updating all Light tables:"
        if self.m_InsteonDevice != None:
            print "lighting.update_insteon"
            self.m_logger.info("Updating Insteon Lights config file.")
            l_dict = {}
            for l_key, l_value in p_lights.iteritems():
                if l_value.get_Family == 'Insteon':
                    print "  ", l_key, " is in family Insteon!", l_value
                    l_dict[l_key] = l_value
            self.m_InsteonDevice.update_all_devices()
        if self.m_UpbDevice != None:
            pass
        if self.m_X10Device != None:
            pass

    def scan_all_lighting(self, p_lights):
        """ *!* 
        """
        if self.m_InsteonDevice != None:
            self.m_InsteonDevice.scan_insteon_devices(p_lights)

    def change_light_setting(self, p_name, p_level = 0, _p_family = None):
        """ *!* 
        Turn a light to a given level (0-100) off/dimmed/on.
        """
        self.m_logger.info("Turn Light {0:} to level {1:}.".format(p_name, p_level))
        l_family = Light_Data[p_name].get_Family()
        if l_family == 'Insteon':
            self.m_InsteonDevice.change_light_setting(p_name, p_level)
        elif l_family == 'UPB':
            self.m_logger.warn("UPB not implemented yet.")
        else:
            self.m_logger.error("No such light family as {0:}.".format(l_family))


class SceneUtility(SceneAPI):

    def clear_scene_data(self):
        self.Scene_Data = {}

    def dump_scene_data(self):
        print " -- lighting.dump_scene_data()"
        for l_key, l_value in self.Scene_Data.iteritems():
            print '   ', l_key, l_value
        print

    def load_scene_data(self):
        self.m_logger.info("Using Scenes.")
        l_dict = self.m_config.get_value('Scenes')
        for l_key, l_value in l_dict.iteritems():
            self.Scene_Data[l_key] = {}
            for l_par, l_var in l_value.iteritems():
                self.Scene_Data[l_key][l_par] = l_var
        return self.Scene_Data

    def update_scene_config(self, p_scene):
        self.m_config.write_scenes(p_scene)


class LightingMain(LightingUtility, SceneUtility, ControllerAPI, ButtonAPI):
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

        #print " - LightingMain 1"
        self.load_all_light_tables()
        #self.dump_all_devices()

        self.clear_scene_data()
        #print " - LightingMain 2"
        self.load_scene_data()
        #self.dump_scene_data()

        #print " - LightingMain 3"
        self.m_logger.info("Initialized.")
        return self

    def __init__(self):
        """Constructor for the component
        """

    def lighting_startup(self):
        #print " @ LightingStartup 1"
        self.startup_all_lighting_modules()

### END
