#!/usr/bin/env python

"""Handle the controller component of the lighting system.

Note that controllers have common light info and also have controller info,
family info, and interface info.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Lighting.lighting_core import ReadWriteConfigXml
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger
from Modules.Drivers import interface
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 1
LOG = Logger.getLogger('PyHouse.Controller     ')



class LCApi(ReadWriteConfigXml):
    """
    Get/Put all the information about one controller:
        Base Light Data
        Controller Data
        Family Data
        Interface Data
    """

    m_count = 0
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _read_base_data(self, p_xml):
        l_obj = ControllerData()
        l_obj = self.read_base_lighting_xml(l_obj, p_xml)
        return l_obj

    def _read_controller_data(self, p_obj, p_xml):
        """
        There are 2 extra fields for controllers - get them.
        """
        p_obj.InterfaceType = self.get_text_from_xml(p_xml, 'InterfaceType')
        p_obj.Port = self.get_text_from_xml(p_xml, 'Port')
        return p_obj

    def _read_family_data(self, p_obj, p_xml):
        l_api = FamUtil().read_family_data(self.m_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    def _read_interface_data(self, p_obj, p_xml):
        try:
            interface.ReadWriteConfigXml().read_interface_xml(p_obj, p_xml)
        except Exception as e_err:  # ControllerFamily invalid or missing
            LOG.error('ERROR - Read Interface Data - {0:} - {1:} - {2:}'.format(e_err, p_obj.Name, p_obj.InterfaceType))

    def read_one_controller_xml(self, p_xml):
        try:
            l_obj = self._read_base_data(p_xml)
            l_obj = self._read_controller_data(l_obj, p_xml)
            l_obj.Key = self.m_count  # Renumber
            self._read_family_data(l_obj, p_xml)
            self._read_interface_data(l_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneController - {0:}'.format(e_err))
        return l_obj

    def read_all_controllers_xml(self, p_controller_sect_xml):
        """Called from lighting.
        """
        self.m_count = 0
        l_dict = {}
        try:
            for l_controller_xml in p_controller_sect_xml.iterfind('Controller'):
                l_controller_obj = self.read_one_controller_xml(l_controller_xml)
                l_dict[self.m_count] = l_controller_obj
                self.m_count += 1
        except AttributeError as e_error:  # No Controller section
            LOG.warning('No Controllers found - {0:}'.format(e_error))
        return l_dict


    def _write_controller_data(self, p_obj, p_xml):
        self.put_text_element(p_xml, 'InterfaceType', p_obj.InterfaceType)
        self.put_text_element(p_xml, 'Port', p_obj.Port)

    def _write_family_data(self, p_controller_obj, p_xml):
        l_api = self.m_pyhouse_obj.House.RefOBJs.FamilyData[p_controller_obj.ControllerFamily].FamilyModuleAPI
        l_api.WriteXml(p_xml, p_controller_obj)

    def _write_interface_data(self, p_obj, p_xml):
        interface.ReadWriteConfigXml().write_interface_xml(p_obj, p_xml)

    def write_one_controller_xml(self, p_controller_obj):
        l_controller_xml = self.write_base_lighting_xml(p_controller_obj)
        self._write_controller_data(p_controller_obj, l_controller_xml)
        self._write_family_data(p_controller_obj, l_controller_xml)
        self._write_interface_data(p_controller_obj, l_controller_xml)
        return l_controller_xml

    def write_controllers_xml(self, p_controller_sect_obj):
        self.m_count = 0
        l_controllers_xml = ET.Element('ControllerSection')
        for l_controller_obj in p_controller_sect_obj.itervalues():
            l_controllers_xml.append(self.write_one_controller_xml(l_controller_obj))
            self.m_count += 1
        return l_controllers_xml

# ## END DBK