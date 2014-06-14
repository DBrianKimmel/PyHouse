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
from Modules.utils import pyh_log
from Modules.drivers import interface
# from src.Modules.utils.tools import PrettyPrintAny

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Controller  ')


class ControllersAPI(lighting_core.CoreAPI):

    m_count = 0
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        super(ControllersAPI, self).__init__()
        self.m_pyhouse_obj = p_pyhouse_obj

    def _read_controller_data(self, p_obj, p_xml):
        p_obj.ControllerInterface = self.get_text_from_xml(p_xml, 'Interface')
        p_obj.Port = self.get_text_from_xml(p_xml, 'Port')

    def _read_family_data(self, p_obj, p_xml):
        l_family = p_obj.LightingFamily
        # PrettyPrintAny(self.m_pyhouse_obj.HouseData, 'HouseData')
        # PrettyPrintAny(self.m_pyhouse_obj.HouseData.FamilyData, 'FamilyData')
        l_api = self.m_pyhouse_obj.HouseData.FamilyData[l_family].ModuleAPI
        l_api.extract_device_xml(p_obj, p_xml)
        # PrettyPrintAny(p_obj, 'Lighting Controller')

    def _read_interface_data(self, p_obj, p_xml):
        interface.ReadWriteConfig().extract_xml(p_obj, p_xml)
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
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')
        self.m_count = 0
        l_dict = {}
        l_sect = p_pyhouse_obj.XmlSection.find('Controllers')
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
        ET.SubElement(l_entry_xml, 'Interface').text = p_controller_obj.ControllerInterface
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
