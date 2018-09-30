"""
-*- test-case-name: PyHouse.src.Modules.Families.X10.test.test_X10_device -*-

@name:      PyHouse/src/Modules/Families/X10/X10_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2017 by D. Brian Kimmel
@note:      Created on Apr 3, 2011
@license:   MIT License
@summary:   This module is for Insteon/X10

"""

__updated__ = '2017-01-20'


# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Computer import logging_pyh as Logger

g_debug = 0
LOG = Logger.getLogger('PyHouse.Dev_X10     ')


class ReadWriteXml(object):
    """Overload the base methods with specific ones here.
    """

    def extract_device_xml(self, p_device_obj, _p_entry_xml):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        if p_device_obj.DeviceFamily == 'Insteon':
            ET.SubElement(p_entry_xml, 'Address').text = p_device_obj.Address
            ET.SubElement(p_entry_xml, 'GroupList').text = str(p_device_obj.GroupList)
            ET.SubElement(p_entry_xml, 'GroupNumber').text = str(p_device_obj.GroupNumber)
        elif p_device_obj.DeviceFamily == 'UPB':
            try:
                ET.SubElement(p_entry_xml, 'Password').text = str(p_device_obj.Password)
                ET.SubElement(p_entry_xml, 'UnitID').text = str(p_device_obj.UnitID)
            except AttributeError:
                pass

    def turn_light_off(self, p_name):
        pass

    def turn_light_on(self, p_name):
        pass

    def turn_light_dim(self, p_name, p_level):
        pass

    def scan_all_lights(self, p_lights):
        pass


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        pass

    def Stop(self):
        pass

    def WriteXml(self, p_xml):
        return p_xml

    def SaveXml(self, p_xml):
        pass

    def ChangeLight(self, p_light_obj, p_source, p_level, p_rate=0):
        pass

# ## END
