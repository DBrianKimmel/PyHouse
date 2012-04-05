#!/usr/bin/python

"""Insteon Device module.

This is the main module for the Insteon family of devices.
it provides the single interface into the 
Several other insteon modules are included by this and are invisible to the other families.

This module loads the information about all the Insteon devices.

InsteonControllers
serial_port

"""

# Import system type stuff
import logging

# Import PyMh files
import configure_mh
import lighting
#from tools import Lister


class InsteonLightingData(lighting.LightingData):
    """Insteon specific data we wish to export.  Extends the LightingData class.
    Create a dict of devices.
    Each device will contain a dict of attributes and vales
    """

    Family = 'Insteon'
    Address = ''
    Code = ''
    GroupList = ''
    GroupNumber = 0
    DevCat = 0x0000
    Controller = True
    Responder = True
    Master = False
    Dimmable = False

    def __init__(self, Name):
        lighting.LightingData.__init__(self, Name)

    def __repr__(self):
        l_str = lighting.LightingData.__repr__(self)
        l_str += " Address: {0:10.10} Controller: {1:}".format(self.Address, self.Controller)
        return l_str

    def get_Address(self):
        return self.Address.upper()

    def get_DevCat(self):
        return self.DevCat

    def XXget_Code(self):
        return self.Code

    def get_GroupList(self):
        return self.GroupList

    def get_GroupNumber(self):
        return self.GroupNumber

    def get_Controller(self):
        return self.Controller

    def get_Responder(self):
        return self.Responder

    def get_Dimmable(self):
        return self.Dimmable

    def get_Master(self):
        return self.Master


class InsteonLightingStatus(lighting.LightingStatus):
    """
    """


class InsteonLightingAPI(lighting.LightingAPI):
    """Interface to the lights of this module.
    """

    def turn_light_on(self, p_name):
        """Turn a light on (level 100).
        """
        self.m_insteonPLM.turn_light_on(p_name)

    def turn_light_off(self, p_name):
        """Turn a light off (level 0).
        """
        self.m_insteonPLM.turn_light_off(p_name)

    def turn_light_dim(self, p_name, p_level):
        """Turn on a light to a given level (1-100).
        """
        self.m_insteonPLM.turn_light_dim(p_name, p_level)

    def dump_all_devices(self):
        print "\nDump all Insteon devices"
        for _l_key, l_value in lighting.Light_Data.iteritems():
            print l_value
        print

    def update_all_devices(self):
        self.write_insteon_lights(lighting.Light_Data)

    def update_all_statuses(self):
        assert 0, "dump all statuses must be subclassed."


class InsteonControllerData(lighting.ControllerData):

    def __init__(self, Name):
        lighting.ControllerData.__init__(self, Name)


class InsteonControllerAPI(lighting.ControllerAPI, InsteonControllerData):
    """
    """

    def load_insteon_controllers(self, p_dict):
        lighting.ControllerAPI.load_all_controllers(self, p_dict)


class InsteonButtonData(lighting.ButtonData):

    def __init__(self, Name):
        lighting.ButtonData.__init__(self, Name)


class InsteonButtonAPI(lighting.ButtonAPI, InsteonButtonData):
    """
    """

    def load_insteon_buttons(self, p_dict):
        lighting.ButtonAPI.load_all_buttons(self, p_dict)
        lighting.ButtonAPI.dump_all_buttons(self)


class LoadSaveInsteonData(InsteonLightingAPI, InsteonControllerAPI, InsteonButtonAPI):

    def build_light_entry(self, p_key, p_dict):
        """convert a config dict entry to a lighting object
        """
        l_light = InsteonLightingData(p_key)
        l_light.Name = p_dict.get('Name', 'NoName')
        l_light.Family = p_dict.get('Family', 'Insteon')
        l_light.Address = p_dict.get('Address', '01.23.45')
        l_light.Type = p_dict.get('Type', None)
        l_light.Comment = p_dict.get('Comment', '')
        l_light.Coords = p_dict.get('Coords', (0, 0))
        l_light.GroupList = p_dict.get('GroupList', '')
        l_light.GroupNumber = p_dict.get('GroupNumber', 0)
        l_light.Room = p_dict.get('Room', None)
        l_light.Controller = p_dict.get('Controller', False)
        l_light.Responder = p_dict.get('Responder', False)
        l_light.Dimmable = p_dict.get('Dimmable', False)
        l_light.DevCat = p_dict.get('DevCat', 0)
        l_light.Master = p_dict.get('Master', True)
        l_light.Code = p_dict.get('Code', '')
        l_light.Responder = p_dict.get('Responder', False)
        lighting.Light_Data[p_key] = l_light

    def extract_insteon_devices(self, p_dict):
        """Create all device entries from the dict.
        
        @param p_dict:All the InsteonLights config dict. 
        @return: the insteon lighting dict.
        """
        for l_key, l_data in p_dict.iteritems():
            self.build_light_entry(l_key, l_data)
            l_status = InsteonLightingStatus(l_key)
            l_status.CurLevel = 0
            lighting.Light_Status[l_key] = l_status
        self.m_logger.info('Insteon Lights loaded.')

    def write_insteon_lights(self, p_lights,):
        """
        """
        l_cfg = {}
        print "  insteon_Device.writing_insteon "
        for l_name, l_obj in p_lights.iteritems():
            if l_obj.get_Family() != 'Insteon': continue
            l_cfg[l_name] = {}
            l_cfg[l_name]['Name'] = l_obj.get_Name()
            l_cfg[l_name]['Family'] = l_obj.get_Family()
            l_cfg[l_name]['Address'] = l_obj.get_Address()
            l_cfg[l_name]['Type'] = l_obj.get_Type()
            l_cfg[l_name]['Comment'] = l_obj.get_Comment()
            l_cfg[l_name]['Room'] = l_obj.get_Room()
            l_cfg[l_name]['Coords'] = l_obj.get_Coords()
            l_cfg[l_name]['GroupList'] = l_obj.get_GroupList()
            l_cfg[l_name]['GroupNumber'] = l_obj.get_GroupNumber()
            l_cfg[l_name]['Controller'] = l_obj.get_Controller()
            l_cfg[l_name]['Responder'] = l_obj.get_Responder()
            l_cfg[l_name]['Dimmable'] = l_obj.get_Dimmable()
            l_cfg[l_name]['DevCat'] = l_obj.get_DevCat()
            l_cfg[l_name]['Master'] = l_obj.get_Master()
            l_cfg[l_name]['Code'] = l_obj.get_Code()
        cfg = configure_mh.ConfigureAPI.get_cfg_file(configure_mh.ConfigureAPI(), './config/Insteon.conf')
        cfg['InsteonLights'] = l_cfg
        cfg.write()


class InsteonDeviceUtility(LoadSaveInsteonData):

    def scan_insteon_devices(self, _p_lights):
        print "insteon_Device.scan_insteon_devices "
        self.m_insteonPLM.scan_all_lights(lighting.Light_Data)

    def change_light_setting(self, p_name, p_level):
        print " insteon_Device.change_light_settings "
        if int(p_level) == 0:
            self.turn_light_off(p_name)
        elif int(p_level) == 100:
            self.turn_light_on(p_name)
        else:
            self.turn_light_dim(p_name, p_level)
        lighting.Light_Status[p_name].CurLevel = p_level


class InsteonDeviceMain(InsteonDeviceUtility):
    """
    """

    m_config = None
    m_logger = None
    m_insteonLink = None
    m_insteonPLM = None

    def __init__(self):
        self.m_config = configure_mh.ConfigureMain()
        self.m_logger = logging.getLogger('PyHouse.InsteonDevice')
        self.load_all_Insteon()
        import Insteon_Link
        self.m_insteonLink = Insteon_Link.InsteonLinkMain()
        import Insteon_PLM
        self.m_insteonPLM = Insteon_PLM.InsteonPLMMain()
        self.m_logger.info('Initialized.')

    def Insteon_startup(self):
        #print " # InteonDevice.Insteon_Startup 1"
        self.m_insteonPLM.PLM_startup()
        self.m_logger.info('Started.')

    def load_all_Insteon(self):
        """Load each section of the Insteon family.
        """
        self.load_insteon_controllers(self.m_config.get_value('InsteonControllers'))
        self.load_insteon_buttons(self.m_config.get_value('InsteonButtons'))
        self.extract_insteon_devices(self.m_config.get_value('InsteonLights'))
        #self.dump_all_devices()

### END
