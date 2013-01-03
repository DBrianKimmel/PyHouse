#!/usr/bin/python

"""Load the database with UPB devices.
"""

# Import system type stuff
import logging

# Import PyMh files
from lighting import lighting


Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data
Light_Data = lighting.Light_Data
Light_Status = lighting.Light_Status

g_debug = 0
g_logger = None
g_pim = None


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

class ButtonData(lighting.ButtonData, CoreData):

    def __init__(self):
        super(ButtonData, self).__init__()

    def __str__(self):
        l_str = super(ButtonData, self).__str__()
        return l_str

class ButtonAPI(lighting.ButtonAPI, CoreAPI):

    def load_all_buttons(self, p_dict):
        """
        @param p_dict: outer layer of all buttons in a dict.
        """
        for l_dict in p_dict.itervalues():
            l_button = ButtonData()
            l_button = self.load_upb_button(l_dict, l_button)
            Button_Data[l_button.Key] = l_button

    def load_upb_button(self, p_dict, p_button):
        l_button = p_button
        l_button = super(ButtonAPI, self).load_button(p_dict, l_button)
        l_button = self.load_device(p_dict, l_button)
        return l_button


class ControllerData(lighting.ControllerData, CoreData):

    def __init__(self):
        super(ControllerData, self).__init__()

    def __str__(self):
        l_str = super(ControllerData, self).__str__()
        return l_str

class ControllerAPI(lighting.ControllerAPI, CoreAPI):

    def load_all_controllers(self, p_dict):
        for l_dict in p_dict.itervalues():
            l_ctlr = ControllerData()
            l_ctlr = self.load_upb_controller(l_dict, l_ctlr)
            Controller_Data[l_ctlr.Key] = l_ctlr

    def load_upb_controller(self, p_dict, p_controller):
        l_ctlr = p_controller
        l_ctlr = super(ControllerAPI, self).load_controller(p_dict, l_ctlr)
        l_ctlr = self.load_device(p_dict, l_ctlr)
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
        for l_dict in p_dict.itervalues():
            l_light = LightingData()
            l_light = self.load_upb_light(l_dict, l_light)
            Light_Data[l_light.Key] = l_light

    def load_upb_light(self, p_dict, p_light):
        l_light = p_light
        l_light = super(LightingAPI, self).load_light(p_dict, l_light)
        l_light = self.load_device(p_dict, l_light)
        return l_light

    def change_light_setting(self, p_obj, p_level):
        g_pim.LightingAPI().change_light_setting(p_obj, p_level)

    def update_all_lights(self):
        pass


class LightingStatusData(lighting.LightingStatusData): pass
class LightingStatusAPI(lighting.LightingStatusAPI, LightingStatusData): pass

class LoadSaveInsteonData(LightingAPI, ControllerAPI, ButtonAPI, LightingStatusAPI): pass


import UPB_Pim


def Init():
    """Constructor for the UPB .
    """
    if g_debug > 0:
        print "Device_UPB.Init()"
    global g_logger, g_pim
    g_logger = logging.getLogger('PyHouse.Device_UPB')
    g_logger.info('Initializing.')
    UPB_Pim.Init()
    g_logger.info('Initialized.')
    g_pim = UPB_Pim

def Start():
    if g_debug > 0:
        print "Device_UPB.Start()"
    g_logger.info('Starting.')
    UPB_Pim.Start()
    g_logger.info('Started.')

def Stop():
    if g_debug > 0:
        print "Device_UPB.Stop()"
    UPB_Pim.Stop()

# ## END
