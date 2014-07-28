"""
-*- test-case-name: PyHouse.Modules.lights.test.test_lighting_core -*-

@name: PyHouse/src/Modules/lights/lighting_core.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Jun 13, 2013
@license: MIT License
@summary: A base class for all things lighting

This is a base class that other lighting modules inherit from.
"""

# Import system type stuff

# Import PyHouse files
from Modules.utils.xml_tools import XmlConfigTools

g_debug = 0


class ReadWriteConfigXml(XmlConfigTools):

    def read_base_lighting_xml(self, p_device_obj, p_entry_xml):
        """This will read all the information in a BaseLightingData object

        @param p_device_obj: is the device we are extracting information for.
        @param p_entry_xml: is the light XML element
        @return: a dict of the entry to be attached to a higher object.
        """
        self.read_base_object_xml(p_device_obj, p_entry_xml)
        p_device_obj.Comment = self.get_text_from_xml(p_entry_xml, 'Comment')
        p_device_obj.ControllerFamily = self.get_text_from_xml(p_entry_xml, 'ControllerFamily')
        p_device_obj.Coords = self.get_text_from_xml(p_entry_xml, 'Coords')
        p_device_obj.IsDimmable = self.get_bool_from_xml(p_entry_xml, 'IsDimmable')
        p_device_obj.LightingType = self.get_text_from_xml(p_entry_xml, 'LightingType')
        p_device_obj.RoomName = self.get_text_from_xml(p_entry_xml, 'RoomName')
        return p_device_obj

    def write_base_lighting_xml(self, p_device_obj):
        l_xml = self.write_base_object_xml('Light', p_device_obj)
        self.put_text_element(l_xml, 'Comment', p_device_obj.Comment)
        self.put_text_element(l_xml, 'ControllerFamily', p_device_obj.ControllerFamily)
        self.put_text_element(l_xml, 'Coords', p_device_obj.Coords)
        self.put_bool_element(l_xml, 'IsDimmable', p_device_obj.IsDimmable)
        self.put_text_element(l_xml, 'LightingType', p_device_obj.LightingType)
        self.put_text_element(l_xml, 'RoomName', p_device_obj.RoomName)
        return l_xml

# ## END DBK
