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
from Modules.utils.xml_tools import ConfigTools
from Modules.web import web_utils


g_debug = 0
# 0 = off


class CoreAPI(ConfigTools):

    def read_base_lighting_xml(self, p_device_obj, p_entry_xml):
        """This will read all the information in a BaseLightingData object

        @param p_device_obj: is the device we are extracting information for.
        @param p_entry_xml: is the light XML element
        @return: a dict of the entry to be attached to a higher object.
        """
        self.read_base_object_xml(p_device_obj, p_entry_xml)
        p_device_obj.Comment = self.get_text_from_xml(p_entry_xml, 'Comment')
        p_device_obj.Coords = self.get_text_from_xml(p_entry_xml, 'Coords')
        p_device_obj.Dimmable = self.get_bool_from_xml(p_entry_xml, 'Dimmable')
        p_device_obj.Family = l_fam = self.get_text_from_xml(p_entry_xml, 'Family')
        p_device_obj.RoomName = p_entry_xml.findtext('Room')
        p_device_obj.Type = p_entry_xml.findtext('Type')
        return p_device_obj

    def write_base_lighting_xml(self, p_entry, p_device_obj):
        self.put_text_element(p_entry, 'Comment', p_device_obj.Comment)
        self.put_text_element(p_entry, 'Coords', p_device_obj.Coords)
        self.put_bool_element(p_entry, 'Dimmable', p_device_obj.Dimmable)
        self.put_text_element(p_entry, 'Family', p_device_obj.Family)
        self.put_text_element(p_entry, 'Room', p_device_obj.RoomName)
        self.put_text_element(p_entry, 'Type', p_device_obj.Type)

# ## END DBK
