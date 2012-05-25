#!/usr/bin/python

"""Load the database with UPB devices.
"""

# Import system type stuff
import logging

# Import PyMh files
import configure_mh
import lighting


Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data
Light_Data = lighting.Light_Data
Light_Status = lighting.Light_Status

m_config = None
m_logger = None


class ButtonData(lighting.ButtonData): pass
class ButtonAPI(lighting.ButtonAPI, ButtonData): pass

class ControllerData(lighting.ControllerData):

    def __init__(self):
        lighting.ControllerData.__init__(self)
        self.Family = 'UPB'
        self.NetworkID = None
        self.Password = None
        self.UnitID = None

    def __repr__(self):
        l_str = lighting.ControllerData.__repr__(self)
        return l_str

    def get_network_id(self):
        return self.__NetworkID
    def set_network_id(self, value):
        self.__NetworkID = value
    def get_password(self):
        return self.__Password
    def set_password(self, value):
        self.__Password = value
    def get_unit_id(self):
        return self.__UnitID
    def set_unit_id(self, value):
        self.__UnitID = value

    NetworkID = property(get_network_id, set_network_id, None, None)
    Password = property(get_password, set_password, None, None)
    UnitID = property(get_unit_id, set_unit_id, None, None)

class ControllerAPI(lighting.ControllerAPI, ControllerData):

    def load_all_controllers(self, p_dict):
        lighting.ControllerAPI.load_all_controllers(self, p_dict)

    def load_controller(self, p_dict):
        l_ctlr = lighting.ControllerAPI.load_controller(self, p_dict)
        l_ctlr.NetworkID = p_dict.get('NetworkID', None)
        l_ctlr.Password = p_dict.get('Password', None)
        l_ctlr.UnitID = p_dict.get('UnitID', None)
        return l_ctlr


class LightingData(lighting.LightingData):

    def __init__(self):
        lighting.LightingData.__init__(self)
        self.Family = 'UPB'
        self.NetworkID = None
        self.Password = None
        self.UnitID = None

    def __repr__(self):
        l_str = lighting.LightingData.__repr__(self)
        return l_str

class LightingAPI(lighting.LightingAPI, LightingData):

    def load_light(self, p_dict):
        l_light = lighting.LightingAPI.load_light(self, p_dict)
        l_light.NetworkID = p_dict.get('NetworkID', None)
        l_light.Password = p_dict.get('Password', None)
        l_light.UnitID = p_dict.get('UnitID', None)
        return l_light

    def change_light_setting(self, p_name, p_level):
        self.m_pim.change_light_setting(p_name, p_level)

    def update_all_lights(self):
        pass


class LightingStatusData(lighting.LightingStatusData): pass
class LightingStatusAPI(lighting.LightingStatusAPI, LightingStatusData): pass

class LoadSaveInsteonData(LightingAPI, ControllerAPI, ButtonAPI, LightingStatusAPI): pass

class DeviceMain(LoadSaveInsteonData):

    def __init__(self):
        """Constructor for the UPB .
        """
        self.m_config = configure_mh.ConfigureMain()
        self.m_logger = logging.getLogger('PyHouse.Device_UPB')
        self.m_logger.info('Initializing.')
        #self.load_all_controllers(self.m_config.get_value('UPBControllers'))
        self.load_all_controllers(configure_mh.ConfigureAPI().get_value('UPBControllers'))
        self.load_all_lights(self.m_config.get_value('UPBLights'))
        self.load_all_buttons(self.m_config.get_value('UPBButtons'))
        import UPB_Pim
        self.m_pim = UPB_Pim.UpbPimMain()
        self.m_logger.info('Initialized.')

    def start(self, p_reactor):
        self.m_reactor = p_reactor
        self.m_logger.info('Starting.')
        self.m_pim.PIM_startup()
        self.m_logger.info('Started.')

### END
