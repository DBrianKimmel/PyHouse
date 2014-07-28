#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import ButtonData
from Modules.lights.lighting_core import ReadWriteConfigXml
from Modules.utils.tools import PrettyPrintAny


g_debug = 0
# 0 = off


class ButtonsAPI(ReadWriteConfigXml):

    m_count = 0

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _read_light_data(self, p_obj, p_xml):
        pass

    def _read_family_data(self, p_obj, p_xml):
        l_family = p_obj.ControllerFamily
        l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[l_family].ModuleAPI
        l_api.extract_device_xml(p_obj, p_xml)

    def read_one_button_xml(self, p_button_xml):
        l_button_obj = ButtonData()
        l_button_obj = self.read_base_lighting_xml(l_button_obj, p_button_xml)
        l_button_obj.Key = self.m_count  # Renumber
        self._read_family_data(l_button_obj, p_button_xml)
        return l_button_obj

    def read_buttons_xml(self, p_button_sect_xml):
        self.m_count = 0
        l_button_dict = {}
        for l_button_xml in p_button_sect_xml.iterfind('Button'):
            l_button_dict[self.m_count] = self.read_one_button_xml(l_button_xml)
            self.m_count += 1
        return l_button_dict

    def write_one_button_xml(self, p_button_obj):
        l_button_xml = self.write_base_object_xml('Button', p_button_obj)
        l_button_xml = self.write_base_lighting_xml(p_button_obj)
        return l_button_xml

    def write_buttons_xml(self, p_buttons_obj):
        self.m_count = 0
        l_buttons_xml = ET.Element('ButtonSection')
        for l_button_obj in p_buttons_obj.itervalues():
            l_entry = self.write_one_button_xml(l_button_obj)
            l_buttons_xml.append(l_entry)
            self.m_count += 1
        return l_buttons_xml


# ## END DBK
