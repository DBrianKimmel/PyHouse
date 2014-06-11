"""
-*- test-case-name: PyHouse.src.Modules.lights.test.test_lighting_lights -*-

@name: PyHouse/src/Modules/lights/lighting_lights.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on May 1, 2011
@license: MIT License
@summary: This module handles the lights component of the lighting system.

Inherit from lighting_core.

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

    def _read_light_data(self, p_obj, p_xml):
        pass

    def _read_family_data(self, p_obj, p_xml):
        l_family = p_obj.LightingLightingFamily
        l_api = self.m_pyhouse_obj.HouseData.FamilyData[l_family].ModuleAPI
        l_api.extract_device_xml(p_obj, p_xml)

    def read_one_light_xml(self, p_light_xml):
        l_light_obj = LightData()
        l_light_obj = self.read_base_lighting_xml(l_light_obj, p_light_xml)
        l_light_obj.Key = self.m_count  # Renumber
        self._read_light_data(l_light_obj, p_light_xml)
        self._read_family_data(l_light_obj, p_light_xml)
        return l_light_obj

    def read_lights_xml(self, p_house_xml):
        self.m_count = 0
        l_lights_dict = {}
        l_sect = p_house_xml.find('Lights')
        try:
            for l_light_xml in l_sect.iterfind('Light'):
                l_lights_dict[self.m_count] = self.read_one_light_xml(l_light_xml)
                self.m_count += 1
        except AttributeError:  # No Lights section
            l_lights_dict = {}
        return l_lights_dict

    def write_one_light_xml(self, p_light_obj):
        l_light_xml = self.write_base_object_xml('Light', p_light_obj)
        self.write_base_lighting_xml(l_light_xml, p_light_obj)
        return l_light_xml

    def write_lights_xml(self, p_lights_obj):
        l_lighting_xml = ET.Element('Lights')
        l_count = 0
        for l_light_obj in p_lights_obj.itervalues():
            l_light_xml = self.write_base_object_xml('Light', l_light_obj)
            self.write_base_lighting_xml(l_light_xml, l_light_obj)
            l_lighting_xml.append(l_light_xml)
            l_count += 1
        return l_lighting_xml

# ## END DBK
