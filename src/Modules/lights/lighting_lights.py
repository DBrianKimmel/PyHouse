"""
-*- test-case-name: PyHouse.src.Modules.lights.test.test_lighting_lights -*-

@name: PyHouse/src/Modules/lights/lighting_lights.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on May 1, 2011
@license: MIT License
@summary: This module handles the lights component of the lighting system.

Each entry should contain enough information to allow functionality of various family of lighting controllers.

Insteon is the first type coded and UPB is to follow.

The real work of controlling the devices is delegated to the modules for that family of devices.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import LightData
from Modules.lights import lighting_core


g_debug = 0
# 0 = off


class LightingAPI(lighting_core.CoreAPI):

    m_count = 0

    def read_one_light_xml(self, p_light_element):
        l_light_obj = LightData()
        l_light_obj = self.read_base_lighting_xml(l_entry, l_light_obj, p_house_obj)
        l_light_obj.Key = self.m_count  # Renumber
        return l_light_obj

    def read_light_xml(self, p_house_obj, p_house_xml):
        self.m_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Lights')
        try:
            l_list = l_sect.iterfind('Light')
            for l_entry in l_list:
                l_light_obj = LightData()
                l_light_obj = self.read_base_lighting_xml(l_entry, l_light_obj, p_house_obj)
                l_light_obj.Key = self.m_count  # Renumber
                l_dict[self.m_count] = l_light_obj
                self.m_count += 1
        except AttributeError:  # No Lights section
            l_dict = {}
        p_house_obj.Lights = l_dict
        return l_dict

    def write_light_xml(self, p_house_obj):
        l_lighting_xml = ET.Element('Lights')
        l_count = 0
        for l_light_obj in p_house_obj.Lights.itervalues():
            l_entry = self.xml_create_common_element('Light', l_light_obj)
            self.write_light_common(l_entry, l_light_obj, p_house_obj)
            l_lighting_xml.append(l_entry)
            l_count += 1
        return l_lighting_xml

# ## END DBK
