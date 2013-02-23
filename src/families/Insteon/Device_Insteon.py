#!/usr/bin/python

"""Insteon Device module.

This is the main module for the Insteon family of devices.
it provides the single interface into the family.
Several other Insteon modules are included by this and are invisible to the other families.

This module loads the information about all the Insteon devices.

InsteonControllers
serial_port

"""

# Import system type stuff
import logging

# Import PyMh files
from lighting import lighting
from house import house


House_Data = house.House_Data

g_debug = 3
g_logger = None


class CoreData (object):
    """This class contains the Insteon specific information about the various devices
    controlled by PyHouse.
    """

    def __init__(self):
        self.Address = None
        self.Controller = None
        self.DevCat = None
        self.Family = 'Insteon'
        self.GroupList = None
        self.GroupNumber = None
        self.Master = None
        self.ProductKey = None
        self.Responder = None

    def __repr__(self):
        l_str = lighting.ControllerData.__repr__(self)
        l_str += " Address: {0:} Controller: {1:}".format(self.get_address(), self.Controller)
        return l_str

    def get_address(self):
        return self.__Address
    def set_address(self, value):
        self.__Address = value
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
    def get_product_key(self):
        return self.__ProductKey
    def set_product_key(self, value):
        self.__ProductKey = value
    def get_responder(self):
        return self.__Responder
    def set_responder(self, value):
        self.__Responder = value

    Address = property(get_address, set_address, None, "'Str' Device Address as 'aa.bb.cc'.")
    Controller = property(get_controller, set_controller, None, "Bool Device can act as a controller of others.")
    DevCat = property(get_dev_cat, set_dev_cat, None, "Int16' Device Category and SubCategory as 0x0123.")
    GroupList = property(get_group_list, set_group_list, None, None)
    GroupNumber = property(get_group_number, set_group_number, None, None)
    Master = property(get_master, set_master, None, "'Bool' ???")
    ProductKey = property(get_product_key, set_product_key, None, "New - Replacing devcat someday perhaps.")
    Responder = property(get_responder, set_responder, None, "'Bool' Device can act as responder from a controller.")


class CoreAPI(object):

    def XXload_device(self, p_dict, p_dev):
        p_dev.Family = 'Insteon'
        p_dev.Address = self.getText(p_dict, 'Address')
        p_dev.Controller = self.getBool(p_dict, 'Controller')
        p_dev.DevCat = self.getInt(p_dict, 'DevCat')
        p_dev.GroupList = self.getText(p_dict, 'GroupList')
        p_dev.GroupNumber = self.getInt(p_dict, 'GroupNumber')
        p_dev.Master = self.getBool(p_dict, 'Master')
        p_dev.ProductKey = self.getInt(p_dict, 'ProductKey')
        p_dev.Responder = self.getBool(p_dict, 'Responder')
        return p_dev


class ButtonData(lighting.ButtonData, CoreData):

    def __init__(self):
        super(ButtonData, self).__init__()

    def __str__(self):
        l_str = super(ButtonData, self).__str__()
        l_str += " Address:{0:}".format(self.get_address())
        return l_str


class ButtonAPI(lighting.ButtonAPI, CoreAPI): pass


class ControllerData(lighting.ControllerData, CoreData):

    def __init__(self):
        super(ControllerData, self).__init__()

    def __str__(self):
        l_str = super(ControllerData, self).__str__()
        l_str += " Address:{0:}".format(self.get_address())
        return l_str


class ControllerAPI(lighting.ControllerAPI, CoreAPI): pass


class LightData(lighting.LightData, CoreData):
    """Insteon specific data we wish to export.  Extends the LightData class
    Create a dict of devices.
    Each device will contain a dict of attributes and vales
    """

    def __init__(self):
        super(LightData, self).__init__()

    def __str__(self):
        l_str = super(LightData, self).__str__()
        l_str += " Address:{0:}".format(self.get_address())
        return l_str

# TODO: Add read write xml for insteon specific data


class LightingAPI(lighting.LightingAPI, CoreAPI):
    """Interface to the lights of this module.
    """

    def change_light_setting(self, p_light_obj, p_level):
        if g_debug > 1:
            print "Device_Insteon.change_light_setting()", p_level, p_light_obj
        if p_light_obj.Family == 'Insteon':
            self.m_plm.change_light_setting(p_light_obj, p_level)


    def scan_all_lights(self, _p_lights):
        if g_debug > 0:
            print "insteon_Device.scan_insteon_devices "
        self.m_plm.scan_all_lights(House_Data)

import Insteon_PLM

class API(LightingAPI):

    m_plm = None

    def __init__(self):
        if g_debug > 0:
            print "Device_Insteon.__init__()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.Device_Insteon')
        g_logger.info('Initializing.')
        self.m_plm = Insteon_PLM.API()
        g_logger.info('Initialized.')


    def Start(self, p_house_obj):
        if g_debug > 0:
            print "Device_Insteon.Start()"
        g_logger.info('Starting.')
        # TODO: for each active Insteon controller, start a PLM for that controller only.
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            # pass
            if l_controller_obj.Family != 'Insteon':
                continue
            if l_controller_obj.Active != True:
                continue
            self.m_plm.Start(p_house_obj, l_controller_obj)
        g_logger.info('Started.')

    def Stop(self):
        if g_debug > 0:
            print "Device_Insteon.Stop()"
        self.m_plm.Stop()

# ## END
