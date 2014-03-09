#!/usr/bin/env python

"""Handle the lights component of the lighting system.

    Each entry should contain enough information to allow functionality of various family of
    lighting controllers.  Insteon is the first type coded and UPB is to follow.

    The real work of controlling the devices is delegated to the modules for that family of devices.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from src.lights import lighting_core
from src.utils import xml_tools


g_debug = 0
# 0 = off


class LightData(lighting_core.CoreData):

    def __init__(self):
        super(LightData, self).__init__()
        self.Controller = None
        self.Type = 'Light'
        self.CurLevel = 0


class LightingAPI(lighting_core.CoreAPI):

    def read_light_xml(self, p_house_obj, p_house_xml):
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Lights')
        try:
            l_list = l_sect.iterfind('Light')
            for l_entry in l_list:
                l_light_obj = LightData()
                l_light_obj = self.read_light_common(l_entry, l_light_obj, p_house_obj)
                l_light_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_light_obj
                l_count += 1
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
