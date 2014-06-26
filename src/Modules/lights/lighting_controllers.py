#!/usr/bin/env python

"""Handle the controller component of the lighting system.

Note that controllers have common light info and also have controller info,
family info, and interface info.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.lights.lighting_core import ReadWriteConfigXml
from Modules.utils import pyh_log
from Modules.drivers import interface
# from Modules.utils.tools import PrettyPrintAny

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Controller  ')


class ControllersAPI(ReadWriteConfigXml):

    m_count = 0
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _read_controller_data(self, p_obj, p_xml):
        p_obj.InterfaceType = self.get_text_from_xml(p_xml, 'InterfaceType')
        p_obj.Port = self.get_text_from_xml(p_xml, 'Port')

    def _read_family_data(self, p_controller_obj, p_xml):
        l_family = p_controller_obj.LightingFamily
        l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[l_family].ModuleAPI
        l_api.extract_device_xml(p_controller_obj, p_xml)
        # PrettyPrintAny(p_controller_obj, 'Lighting Controller')

    def _read_interface_data(self, p_obj, p_xml):
        interface.ReadWriteConfigXml().extract_xml(p_obj, p_xml)
        pass

    def read_one_controller_xml(self, p_controller_xml):
        """
        Get all the information about one controller:
            Base Light Data
            Controller Data
            Family Data
            Interface Data
        """
        l_controller_obj = ControllerData()
        l_controller_obj = self.read_base_lighting_xml(l_controller_obj, p_controller_xml)
        l_controller_obj.Key = self.m_count  # Renumber
        self._read_controller_data(l_controller_obj, p_controller_xml)
        self._read_family_data(l_controller_obj, p_controller_xml)
        self._read_interface_data(l_controller_obj, p_controller_xml)
        # PrettyPrintAny(l_controller_obj, 'Controller')
        return l_controller_obj

    def read_controllers_xml(self, p_pyhouse_obj):
        """Called from lighting.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_count = 0
        l_dict = {}
        l_house_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        l_controllers_xml = l_house_xml.find('ControllerSection')
        # PrettyPrintAny(l_controllers_xml, 'Lighting Controllers')
        try:
            for l_controller_xml in l_controllers_xml.iterfind('Controller'):
                l_controller_obj = self.read_one_controller_xml(l_controller_xml)
                l_dict[self.m_count] = l_controller_obj
                self.m_count += 1
        except AttributeError as e_error:  # No Controller section
            print('Lighting Controllers - No Controllers found - {0:}'.format(e_error))
            l_dict = {}
        return l_dict

    def write_one_controller_xml(self, p_controller_obj):
        l_entry_xml = self.write_base_object_xml('Controller', p_controller_obj)
        self.write_base_lighting_xml(l_entry_xml, p_controller_obj)
        ET.SubElement(l_entry_xml, 'InterfaceType').text = p_controller_obj.InterfaceType
        ET.SubElement(l_entry_xml, 'Port').text = p_controller_obj.Port
        interface.ReadWriteConfigXml().write_xml(l_entry_xml, p_controller_obj)
        return l_entry_xml

    def write_controllers_xml(self, p_controllers_obj):
        print('lighting_controllers.write_controllers_xml')
        l_count = 0
        l_controllers_xml = ET.Element('ControllerSection')
        for l_controller_obj in p_controllers_obj.itervalues():
            l_entry_xml = self.write_one_controller_xml(l_controller_obj)
            l_controllers_xml.append(l_entry_xml)
            l_count += 1
        return l_controllers_xml

# ## END DBK
