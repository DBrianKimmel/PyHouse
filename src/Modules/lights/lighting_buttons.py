#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import ButtonData
from Modules.lights import lighting_core


g_debug = 0
# 0 = off


class ButtonsAPI(lighting_core.CoreAPI):

    def __init__(self):
        super(ButtonsAPI, self).__init__()

    def read_button_xml(self, p_house_obj, p_house_xml):
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Buttons')
        try:
            l_list = l_sect.iterfind('Button')
            for l_entry in l_list:
                l_button_obj = ButtonData()
                l_button_obj = self.read_base_lighting_xml(l_entry, l_button_obj, p_house_obj)
                l_button_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_button_obj
                l_count += 1
        except AttributeError:  # No Buttons section
            l_dict = {}
        p_house_obj.Buttons = l_dict
        return l_dict

    def write_button_xml(self, p_house_obj):
        l_count = 0
        l_buttons_xml = ET.Element('Buttons')
        for l_button_obj in p_house_obj.Buttons.itervalues():
            l_entry = self.xml_create_common_element('Button', l_button_obj)
            self.write_light_common(l_entry, l_button_obj, p_house_obj)
            l_buttons_xml.append(l_entry)
            l_count += 1
        return l_buttons_xml


# ## END DBK
