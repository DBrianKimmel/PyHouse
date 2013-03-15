#!/usr/bin/python

"""Load the database with UPB devices.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
from lights import lighting

g_debug = 0

g_logger = None
g_PIM = None
g_house_obj = None


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
        if g_debug > 1:
            print "Device_UPB.load_all_buttons()"
        for l_dict in p_dict.itervalues():
            l_button = ButtonData()
            l_button = self.load_upb_button(l_dict, l_button)
            g_house_obj.Buttons[l_button.Key] = l_button

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
        if g_debug > 1:
            print "Device_UPB.load_all_controllers()"
        for l_dict in p_dict.itervalues():
            l_ctlr = ControllerData()
            l_ctlr = self.load_upb_controller(l_dict, l_ctlr)
            g_house_obj.Controllers[l_ctlr.Key] = l_ctlr

    def load_upb_controller(self, p_dict, p_controller):
        l_ctlr = p_controller
        l_ctlr = super(ControllerAPI, self).load_controller(p_dict, l_ctlr)
        l_ctlr = self.load_device(p_dict, l_ctlr)
        return l_ctlr


class LightData(lighting.LightData, CoreData):

    def __init__(self):
        super(LightData, self).__init__()

    def __str__(self):
        l_str = super(LightData, self).__str__()
        return l_str

class LightingAPI(lighting.LightingAPI, CoreAPI):
    """Interface to the lights of this module.
    """

    def extract_device_xml(self, p_entry_xml, p_device_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        p_device_obj.NetworkID = p_entry_xml.findtext('NetworkID')
        p_device_obj.Password = p_entry_xml.findtext('Password')
        p_device_obj.UnitID = p_entry_xml.findtext('UnitID')
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        try:
            ET.SubElement(p_entry_xml, 'NetworkID').text = self.put_str(p_device_obj.NetworkID)
            ET.SubElement(p_entry_xml, 'Password').text = str(p_device_obj.Password)
            ET.SubElement(p_entry_xml, 'UnitID').text = str(p_device_obj.UnitID)
        except AttributeError:
            pass

    def load_all_lights(self, p_dict):
        if g_debug > 1:
            print "Device_UPB.load_all_lights()", p_dict
        for l_dict in p_dict.itervalues():
            l_light = LightData()
            l_light = self.load_upb_light(l_dict, l_light)
            g_house_obj.Lights[l_light.Key] = l_light

    def load_upb_light(self, p_dict, p_light):
        if g_debug > 1:
            print "Device_UPB.load_upb_light()"
        l_light = p_light
        l_light = super(LightingAPI, self).load_light(p_dict, l_light)
        l_light = self.load_device(p_dict, l_light)
        return l_light

    def change_light_setting(self, p_light_obj, p_level):
        if g_debug > 1:
            print "Device_UPB.change_light_setting()"
        if p_light_obj.Family == 'UPB':
            g_PIM.change_light_setting(p_light_obj, p_level)

    def update_all_lights(self):
        if g_debug > 1:
            print "Device_UPB.update_all_lights()"


class LoadSaveInsteonData(LightingAPI, ControllerAPI, ButtonAPI): pass


import UPB_Pim


class API(LightingAPI):

    def __init__(self):
        """Constructor for the UPB .
        """
        if g_debug > 0:
            print "Device_UPB.__init__()"
        global g_logger, g_PIM
        g_logger = logging.getLogger('PyHouse.Device_UPB')
        g_logger.info('Initializing.')
        g_PIM = self.m_pim = UPB_Pim.API()
        g_logger.info('Initialized.')

    def Start(self, p_house_obj):
        if g_debug > 0:
            print "Device_UPB.Start()"
        global g_house_obj
        g_house_obj = p_house_obj
        g_logger.info('Starting.')
        self.m_pim.Start(p_house_obj)
        g_logger.info('Started.')

    def Stop(self, p_xml):
        if g_debug > 0:
            print "Device_UPB.Stop()"
        self.m_pim.Stop()
        return p_xml

    def SpecialTest(self):
        if g_debug > 0:
            print "Device_UPB.API.SpecialTest()"

# ## END
