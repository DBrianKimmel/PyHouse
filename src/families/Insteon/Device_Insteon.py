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
import xml.etree.ElementTree as ET

# Import PyMh files
from lights import lighting

g_debug = 0
g_logger = None


class CoreData (object):
    """This class contains the Insteon specific information about the various devices
    controlled by PyHouse.
    """

    def __init__(self):
        self.Address = ''
        self.Controller = False
        self.DevCat = 0
        self.Family = 'Insteon'
        self.GroupList = ''
        self.GroupNumber = 0
        self.Master = False
        self.ProductKey = ''
        self.Responder = False

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

    def extract_device_xml(self, p_entry_xml, p_device_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        p_device_obj.Address = p_entry_xml.findtext('Address')
        p_device_obj.Controller = p_entry_xml.findtext('Controller')
        p_device_obj.DevCat = p_entry_xml.findtext('DevCat')
        p_device_obj.GroupList = p_entry_xml.findtext('GroupList')
        p_device_obj.GroupNumber = p_entry_xml.findtext('GroupNumber')
        p_device_obj.Master = p_entry_xml.findtext('Master')
        p_device_obj.ProductKey = p_entry_xml.findtext('ProductKey')
        p_device_obj.Responder = p_entry_xml.findtext('Responder')
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        ET.SubElement(p_entry_xml, 'Address').text = p_device_obj.Address
        ET.SubElement(p_entry_xml, 'Controller').text = self.put_bool(p_device_obj.Controller)
        ET.SubElement(p_entry_xml, 'DevCat').text = str(p_device_obj.DevCat)
        ET.SubElement(p_entry_xml, 'GroupList').text = str(p_device_obj.GroupList)
        ET.SubElement(p_entry_xml, 'GroupNumber').text = str(p_device_obj.GroupNumber)
        ET.SubElement(p_entry_xml, 'Master').text = str(p_device_obj.Master)
        ET.SubElement(p_entry_xml, 'ProductKey').text = str(p_device_obj.ProductKey)
        ET.SubElement(p_entry_xml, 'Responder').text = self.put_bool(p_device_obj.Responder)

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
        self.m_house_obj = p_house_obj
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            # pass
            if l_controller_obj.Family != 'Insteon':
                continue
            if l_controller_obj.Active != True:
                continue
            self.m_plm.Start(p_house_obj, l_controller_obj)
        g_logger.info('Started.')

    def Stop(self, p_xml):
        if g_debug > 0:
            print "Device_Insteon.Stop()"
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if l_controller_obj.Family != 'Insteon':
                    continue
                if l_controller_obj.Active != True:
                    continue
                self.m_plm.Stop(l_controller_obj)
        except AttributeError:
            pass  # no controllers for house(House is being added)
        return p_xml

    def SpecialTest(self):
        if g_debug > 0:
            print "Device_Insteon.API.SpecialTest()"
        self.m_plm.SpecialTest()

# ## END
