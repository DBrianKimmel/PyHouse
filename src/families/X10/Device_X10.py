#!/usr/bin/python

"""Load the database with X10 devices.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
from src.lights import lighting


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Startup Details
# 3 = Minor routines

g_logger = None


class X10LightingData(lighting.LightData):

    def __init__(self):
        lighting.LightData.__init__(self)
        self.set_family("X10")
        self.Address = 'asdf'


class LightingAPI(lighting.LightingAPI):
    """Overload the base methods with specific ones here.
    """

    def extract_device_xml(self, _p_entry_xml, p_device_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        if p_device_obj.Family == 'Insteon':
            if g_debug > 4:
                print "WriteLightCommon Insteon=", p_device_obj
            ET.SubElement(p_entry_xml, 'Address').text = p_device_obj.Address
            ET.SubElement(p_entry_xml, 'Controller').text = self.put_bool(p_device_obj.Controller)
            ET.SubElement(p_entry_xml, 'DevCat').text = str(p_device_obj.DevCat)
            ET.SubElement(p_entry_xml, 'GroupList').text = str(p_device_obj.GroupList)
            ET.SubElement(p_entry_xml, 'GroupNumber').text = str(p_device_obj.GroupNumber)
            ET.SubElement(p_entry_xml, 'Master').text = str(p_device_obj.Master)
            ET.SubElement(p_entry_xml, 'ProductKey').text = str(p_device_obj.ProductKey)
            ET.SubElement(p_entry_xml, 'Responder').text = self.put_bool(p_device_obj.Responder)
        elif p_device_obj.Family == 'UPB':
            if g_debug > 4:
                print "WriteLightCommon UPB=", p_device_obj
            try:
                ET.SubElement(p_entry_xml, 'NetworkID').text = self.put_str(p_device_obj.NetworkID)
                ET.SubElement(p_entry_xml, 'Password').text = str(p_device_obj.Password)
                ET.SubElement(p_entry_xml, 'UnitID').text = str(p_device_obj.UnitID)
            except AttributeError:
                pass

    def change_light_setting(self, p_light_obj, p_level, p_house_obj):
        pass

    def update_all_lights(self):
        pass

    def turn_light_off(self, p_name):
        print "Turning off X10 light {0:}".format(p_name)

    def turn_light_on(self, p_name):
        print "Turning on X10 light {0:}".format(p_name)

    def turn_light_dim(self, p_name, p_level):
        print "Turning X10 light {0:} to level {1:}".format(p_name, p_level)

    def scan_all_lights(self, p_lights):
        pass


class API(object):

    def __init__(self, p_house_obj):
        """Constructor for the PLM.
        """
        global g_logger
        g_logger = logging.getLogger('PyHouse.Dev_X10 ')
        self.m_house_obj = p_house_obj
        if g_debug > 0:
            print "Device_X10.__init__()"
        g_logger.info('Initialized.')

    def Start(self, _p_house_obj):
        if g_debug > 0:
            print "Device_X10.Start()"
        g_logger.info('Starting.')
        g_logger.info('Started.')

    def Stop(self, p_xml):
        if g_debug > 0:
            print "Device_X10.Stop()"
        return p_xml

    def SpecialTest(self):
        if g_debug > 0:
            print "Device_X10.API.SpecialTest()"

# ## END
