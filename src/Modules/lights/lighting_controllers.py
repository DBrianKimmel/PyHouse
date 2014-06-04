#!/usr/bin/env python

"""Handle the controller component of the lighting system.

Note that controllers have common light info and also have controller info,
family info, and interface info.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.lights import lighting_core
from Modules.drivers import interface


g_debug = 9


class ControllersAPI(lighting_core.CoreAPI):

    m_count = 0

    def __init__(self):
        super(ControllersAPI, self).__init__()

    def read_family_data(self, p_controller_obj, p_controller_xml):
        l_family = p_controller_obj.Family
        pass

    def read_one_controller_xml(self, p_controller_xml):
        l_controller_obj = ControllerData()
        l_controller_obj = self.read_base_lighting_xml(l_controller_obj, p_controller_xml)
        self.read_family_data(l_controller_obj, p_controller_xml)
        l_controller_obj.Key = self.m_count  # Renumber
        l_controller_obj.Interface = self.get_text_from_xml(p_controller_xml, 'Interface')
        l_controller_obj.Port = self.get_text_from_xml(p_controller_xml, 'Port')
        interface.ReadWriteConfig().extract_xml(l_controller_obj, p_controller_xml)
        if g_debug >= 8:
            print('LC Name: {0:}'.format(l_controller_obj.Name))
        return l_controller_obj

    def read_controllers_xml(self, p_house_xml):
        self.m_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Controllers')
        try:
            for l_controller_xml in l_sect.iterfind('Controller'):
                l_controller_obj = self.read_one_controller_xml(l_controller_xml)
                l_dict[self.m_count] = l_controller_obj
                self.m_count += 1
        except AttributeError:  # No Controller section
            l_dict = {}
        return l_dict

    def write_one_controller_xml(self, p_controller_obj):
        l_entry_xml = self.write_base_object_xml('Controller', p_controller_obj)
        self.write_base_lighting_xml(l_entry_xml, p_controller_obj)
        ET.SubElement(l_entry_xml, 'Interface').text = p_controller_obj.Interface
        ET.SubElement(l_entry_xml, 'Port').text = p_controller_obj.Port
        interface.ReadWriteConfig().write_xml(l_entry_xml, p_controller_obj)
        return l_entry_xml

    def write_controllers_xml(self, p_controllers_obj):
        l_count = 0
        l_controllers_xml = ET.Element('Controllers')
        for l_controller_obj in p_controllers_obj.itervalues():
            l_entry_xml = self.write_one_controller_xml(l_controller_obj)
            l_controllers_xml.append(l_entry_xml)
            l_count += 1
        return l_controllers_xml

# ## END DBK
