#!/usr/bin/env python

"""Handle the controller component of the lighting system.

Note that controllers have common light info and also have controller info,
family info, and interface info.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.lights import lighting_core
from Modules.drivers import interface
from Modules.Core.data_objects import ControllerData


g_debug = 0
# 0 = off


class ControllersAPI(lighting_core.CoreAPI):

    def __init__(self):
        super(ControllersAPI, self).__init__()

    def read_controller_xml(self, p_house_obj, p_house_xml):
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Controllers')
        try:
            l_list = l_sect.iterfind('Controller')
            for l_controller_xml in l_list:
                l_controller_obj = ControllerData()
                l_controller_obj = self.read_light_common(l_controller_xml, l_controller_obj, p_house_obj)
                l_controller_obj.Key = l_count  # Renumber
                l_controller_obj.Interface = self.get_text_from_xml(l_controller_xml, 'Interface')
                l_controller_obj.Port = self.get_text_from_xml(l_controller_xml, 'Port')
                interface.ReadWriteConfig().extract_xml(l_controller_obj, l_controller_xml)
                l_dict[l_count] = l_controller_obj
                l_count += 1
        except AttributeError:  # No Controller section
            l_dict = {}
        p_house_obj.Controllers = l_dict
        return l_dict

    def write_controller_xml(self, p_house_obj):
        l_count = 0
        l_controllers_xml = ET.Element('Controllers')
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            l_entry = self.xml_create_common_element('Controller', l_controller_obj)
            self.write_light_common(l_entry, l_controller_obj, p_house_obj)
            ET.SubElement(l_entry, 'Interface').text = l_controller_obj.Interface
            ET.SubElement(l_entry, 'Port').text = l_controller_obj.Port
            interface.ReadWriteConfig().write_xml(l_entry, l_controller_obj)
            l_controllers_xml.append(l_entry)
            l_count += 1
        return l_controllers_xml

# ## END DBK
