#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import ButtonData
from Modules.lights import lighting_core
# from Modules.utils.tools import PrettyPrintAny


g_debug = 0
# 0 = off


class ButtonsAPI(lighting_core.LightingCoreAPI):

    m_count = 0

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _read_light_data(self, p_obj, p_xml):
        pass

    def _read_family_data(self, p_obj, p_xml):
        l_family = p_obj.LightingFamily
        l_api = self.m_pyhouse_obj.HouseData.FamilyData[l_family].ModuleAPI
        l_api.extract_device_xml(p_obj, p_xml)

    def read_one_button_xml(self, p_button_xml):
        l_button_obj = ButtonData()
        l_button_obj = self.read_base_lighting_xml(l_button_obj, p_button_xml)
        l_button_obj.Key = self.m_count  # Renumber
        self._read_controller_data(l_button_obj, p_button_xml)
        self._read_family_data(l_button_obj, p_button_xml)
        return l_button_obj

    def read_buttons_xml(self, p_pyhouse_obj):
        self.m_count = 0
        l_button_dict = {}
        l_house_xml = p_pyhouse_obj.XmlRoot.find('Houses/House')
        l_buttons_xml = l_house_xml.find('Buttons')
        # PrettyPrintAny(l_buttons_xml, 'Lighting Buttons')
        try:
            for l_button_xml in l_buttons_xml.iterfind('Button'):
                l_button_dict[self.m_count] = self.read_one_button_xml(l_button_xml)
                self.m_count += 1
        except AttributeError:  # No Buttons section
            l_button_dict = {}
        return l_button_dict

    def write_one_button_xml(self, p_button_obj):
        l_button_xml = self.write_base_object_xml('Controller', p_button_obj)
        self.write_base_lighting_xml(l_button_xml, p_button_obj)
        return l_button_xml

    def write_buttons_xml(self, p_buttons_obj):
        self.m_count = 0
        l_buttons_xml = ET.Element('Buttons')
        for l_button_obj in p_buttons_obj.itervalues():
            l_entry = self.write_one_button_xml(l_button_obj)
            l_buttons_xml.append(l_entry)
            self.m_count += 1
        return l_buttons_xml


# ## END DBK
