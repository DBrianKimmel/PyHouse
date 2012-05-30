#!/usr/bin/python

"""Load the database with UPB devices.
"""

# Import system type stuff
import logging

# Import PyMh files
import configure_mh
import lighting
import lighting_tools


Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data
Light_Data = lighting.Light_Data
Light_Status = lighting.Light_Status

m_config = None
m_logger = None


class CoreData(object):

    def __init__(self):
        self.Family = 'UPB'
        self.NetworkID = None
        self.Password = None
        self.UnitID = None

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

class CoreAPI(object):

    def load_device(self, p_dict, p_dev):
        l_dev = p_dev
        l_dev.NetworkID = self.getInt(p_dict, 'NetworkID')
        l_dev.Password = self.getInt(p_dict, 'Password')
        l_dev.UnitID = self.getInt(p_dict, 'UnitID')
        return l_dev

class ButtonData(lighting.ButtonData, CoreData): pass
class ButtonAPI(lighting.ButtonAPI, CoreAPI):

    def load_all_buttons(self, p_dict):
        """
        @param p_dict: outer layer of all buttons in a dict.
        """
        #print " U load_all_buttons"
        for l_key, l_dict in p_dict.iteritems():
            l_button = ButtonData()
            l_button = self.load_upb_button(l_dict, l_button)
            Button_Data[l_button.Key] = l_button
        #print " U Loaded all buttons\n"

    def load_upb_button(self, p_dict, p_button):
        #print " U Insteon load_insteon_button() begin"
        l_button = p_button
        l_button = super(ButtonAPI, self).load_button(p_dict, l_button)
        l_button = self.load_device(p_dict, l_button)
        #print " U Loaded button {0:} -------".format(l_button.Name)
        return l_button


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
        #print " U load_all_controllers"
        for l_key, l_dict in p_dict.iteritems():
            l_ctlr = ControllerData()
            l_ctlr = self.load_upb_controller(l_dict, l_ctlr)
            Controller_Data[l_ctlr.Key] = l_ctlr
        #print " U Loaded all controllers\n"

    def load_upb_controller(self, p_dict, p_controller):
        #print " U load_upb_controller() begin"
        l_ctlr = p_controller
        l_ctlr = super(ControllerAPI, self).load_controller(p_dict, l_ctlr)
        l_ctlr = self.load_device(p_dict, l_ctlr)
        #print " U Loaded controller {0:} -------".format(l_ctlr.Name)
        return l_ctlr


class LightingData(lighting.LightingData, CoreData):

    def __init__(self):
        super(LightingData, self).__init__()

    def __str__(self):
        l_str = super(LightingData, self).__str__()
        return l_str

class LightingAPI(lighting.LightingAPI, CoreAPI):
    """Interface to the lights of this module.
    """

    def load_all_lights(self, p_dict):
        #print " U load_all_lights"
        for l_key, l_dict in p_dict.iteritems():
            l_light = LightingData()
            l_light = self.load_upb_light(l_dict, l_light)
            Light_Data[l_light.Key] = l_light
        #print " U Loaded all lights\n"

    def load_upb_light(self, p_dict, p_light):
        l_light = p_light
        l_light = super(LightingAPI, self).load_light(p_dict, l_light)
        l_light = self.load_device(p_dict, l_light)
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
        #print " U About to Load all UPB Buttons"
        self.load_all_buttons(self.m_config.get_value('UPBButtons'))
        #self.dump_all_buttons()
        #print " U About to Load all UPB Controllers"
        self.load_all_controllers(self.m_config.get_value('UPBControllers'))
        #self.dump_all_controllers()
        #print " U About to Load all UPB Lights"
        self.load_all_lights(self.m_config.get_value('UPBLights'))
        #self.dump_all_lights()
        import UPB_Pim
        self.m_pim = UPB_Pim.UpbPimMain()
        self.m_logger.info('Initialized.')

    def start(self, p_reactor):
        self.m_reactor = p_reactor
        self.m_logger.info('Starting.')
        self.m_pim.PIM_start(p_reactor)
        self.m_logger.info('Started.')

    def stop(self):
        self.m_pim.stop()

### END
