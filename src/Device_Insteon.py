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

Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data
Light_Data = lighting.Light_Data
Light_Status = lighting.Light_Status


class CoreData (object):

    def __init__(self):
        #super(LightingData, self).__init__()
        self.Address = None
        self.Code = None
        self.Controller = None
        self.DevCat = None
        self.Family = 'Insteon-1'
        self.GroupList = None
        self.GroupNumber = None
        self.Master = None
        self.Responder = None

    def __str__(self):
        l_str = lighting.ControllerData.__repr__(self)
        l_str += " Address: {0:} Controller: {1:}".format(self.get_address(), self.Controller)
        return l_str

    def get_address(self):
        return self.__Address
    def set_address(self, value):
        self.__Address = value
    def get_code(self):
        return self.__Code
    def set_code(self, value):
        self.__Code = value
    def get_controller(self):
        return self.__Controller
    def set_controller(self, value):
        self.__Controller = value
    def get_dev_cat(self):
        return self.__DevCat
    def set_dev_cat(self, value):
        self.__DevCat = value
    def get_group_list(self):
        return self.__GroupList
    def set_group_list(self, value):
        self.__GroupList = value
    def get_group_number(self):
        return self.__GroupNumber
    def set_group_number(self, value):
        self.__GroupNumber = value
    def get_master(self):
        return self.__Master
    def set_master(self, value):
        self.__Master = value
    def get_responder(self):
        return self.__Responder
    def set_responder(self, value):
        self.__Responder = value

    Address = property(get_address, set_address, None, "Device Address as string 'aa.bb.cc'.")
    Code = property(get_code, set_code, None, None)
    Controller = property(get_controller, set_controller, None, None)
    DevCat = property(get_dev_cat, set_dev_cat, None, 'Device Category and SubCategory as 0x0123.')
    GroupList = property(get_group_list, set_group_list, None, None)
    GroupNumber = property(get_group_number, set_group_number, None, None)
    Master = property(get_master, set_master, None, None)
    Responder = property(get_responder, set_responder, None, None)

class CoreAPI(object):

    def load_device(self, p_dict, p_dev):
        l_dev = p_dev
        l_dev.Family = 'Insteon'
        l_dev.Address = self.getText(p_dict, 'Address')
        l_dev.Code = self.getText(p_dict, 'Code')
        l_dev.Controller = self.getBool(p_dict, 'Controller')
        l_dev.DevCat = self.getInt(p_dict, 'DevCat')
        l_dev.GroupList = self.getText(p_dict, 'GroupList')
        l_dev.GroupNumber = self.getInt(p_dict, 'GroupNumber')
        l_dev.Master = self.getBool(p_dict, 'Master')
        l_dev.Responder = self.getBool(p_dict, 'Responder')
        #print " I Insteon Load device - {0:}".format(l_dev.Name)
        return l_dev


class ButtonData(lighting.ButtonData, CoreData):

    def __init__(self):
        #print " I Insteon ButtonData.__init_()"
        super(ButtonData, self).__init__()

    def __str__(self):
        l_str = super(ButtonData, self).__str__()
        l_str += " Address:{0:}".format(self.get_address())
        return l_str

class ButtonAPI(lighting.ButtonAPI, CoreAPI):

    def load_all_buttons(self, p_dict):
        """
        @param p_dict: outer layer of all buttons in a dict.
        """
        #print " I load_all_buttons"
        for l_key, l_dict in p_dict.iteritems():
            l_button = ButtonData()
            l_button = self.load_insteon_button(l_dict, l_button)
            Button_Data[l_button.Key] = l_button
        #print " I Loaded all buttons\n"

    def load_insteon_button(self, p_dict, p_button):
        #print " I load_insteon_button() begin"
        l_button = p_button
        l_button = super(ButtonAPI, self).load_button(p_dict, l_button)
        l_button = self.load_device(p_dict, l_button)
        #print " I Loaded button {0:} -------".format(l_button.Name)
        return l_button


class ControllerData(lighting.ControllerData, CoreData):

    def __init__(self):
        super(ControllerData, self).__init__()

    def __str__(self):
        l_str = super(ControllerData, self).__str__()
        l_str += " Address:{0:}".format(self.get_address())
        return l_str

class ControllerAPI(lighting.ControllerAPI, CoreAPI):

    def load_all_controllers(self, p_dict):
        #print " I load_all_controllers"
        for l_key, l_dict in p_dict.iteritems():
            l_ctlr = ControllerData()
            l_ctlr = self.load_insteon_controller(l_dict, l_ctlr)
            Controller_Data[l_ctlr.Key] = l_ctlr
        #print " I Loaded all controllers\n"

    def load_insteon_controller(self, p_dict, p_controller):
        #print " I load_insteon_controller() begin"
        l_ctlr = p_controller
        l_ctlr = super(ControllerAPI, self).load_controller(p_dict, l_ctlr)
        l_ctlr = self.load_device(p_dict, l_ctlr)
        #print " I Loaded controller {0:} -------".format(l_ctlr.Name)
        return l_ctlr


class LightingData(lighting.LightingData, CoreData):
    """Insteon specific data we wish to export.  Extends the LightingData class.
    Create a dict of devices.
    Each device will contain a dict of attributes and vales
    """

    def __init__(self):
        #print " I Insteon LightingData.__init_()"
        super(LightingData, self).__init__()

    def __str__(self):
        l_str = super(LightingData, self).__str__()
        l_str += " Address:{0:}".format(self.get_address())
        return l_str

class LightingAPI(lighting.LightingAPI, CoreAPI):
    """Interface to the lights of this module.
    """

    def load_all_lights(self, p_dict):
        #print " I load_all_lights"
        for l_key, l_dict in p_dict.iteritems():
            l_light = LightingData()
            l_light = self.load_insteon_light(l_dict, l_light)
            Light_Data[l_light.Key] = l_light
        #print " I Loaded all lights\n"

    def load_insteon_light(self, p_dict, p_light):
        #print " I load_insteon_light() begin"
        l_light = p_light
        l_light = super(LightingAPI, self).load_light(p_dict, l_light)
        l_light = self.load_device(p_dict, l_light)
        #print " I Loaded light {0:} -------".format(l_light.Name)
        return l_light

    def change_light_setting(self, p_name, p_level):
        self.m_insteonPLM.change_light_setting(p_name, p_level)

    def update_all_lights(self):
        self.write_insteon_lights(lighting.Light_Data)


class LightingStatusData(lighting.LightingStatusData): pass

class LightingStatusAPI(lighting.LightingStatusAPI, LightingStatusData): pass


class LoadSaveInsteonData(LightingAPI, ControllerAPI, ButtonAPI, LightingStatusAPI):

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

    def scan_all_lights(self, _p_lights):
        print "insteon_Device.scan_insteon_devices "
        self.m_insteonPLM.scan_all_lights(lighting.Light_Data)


class DeviceMain(InsteonDeviceUtility):

    m_config = None
    m_logger = None
    m_insteonLink = None
    m_insteonPLM = None

    def __init__(self):
        self.m_config = configure_mh.ConfigureMain()
        self.m_logger = logging.getLogger('PyHouse.Device_Insteon')
        self.m_logger.info('Initializing.')
        #print " I About to Load all Insteon Buttons"
        self.load_all_buttons(self.m_config.get_value('InsteonButtons'))
        #self.dump_all_buttons()
        #print " I Loading Insteon Controllers"
        self.load_all_controllers(self.m_config.get_value('InsteonControllers'))
        #self.dump_all_controllers()
        self.load_all_lights(self.m_config.get_value('InsteonLights'))
        #self.dump_all_lights()
        self.load_all_status(self.m_config.get_value('InsteonLights'))
        #self.dump_all_status()
        import Insteon_Link
        self.m_insteonLink = Insteon_Link.InsteonLinkMain()
        import Insteon_PLM
        self.m_insteonPLM = Insteon_PLM.InsteonPLMMain()
        self.m_logger.info('Initialized.')

    def start(self, p_reactor):
        self.m_reactor = p_reactor
        self.m_logger.info('Starting.')
        self.m_insteonPLM.start(p_reactor)
        self.m_logger.info('Started.')

    def stop(self):
        self.m_insteonPLM.stop()

### END
