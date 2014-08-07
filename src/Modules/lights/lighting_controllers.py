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
from Modules.families import family
# from Modules.utils.tools import PrettyPrintAny

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Controller  ')


class ControllersAPI(ReadWriteConfigXml):
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

    def _read_controller_data(self, p_xml):
        l_obj = ControllerData()
        l_obj = self.read_base_lighting_xml(l_obj, p_xml)
        l_obj.InterfaceType = self.get_text_from_xml(p_xml, 'InterfaceType')
        l_obj.Port = self.get_text_from_xml(p_xml, 'Port')
        return l_obj

    def _read_family_data(self, p_controller_obj, p_xml):
        """
        Read and fill in the family specific data of the controller.
        """
        # l_family = p_controller_obj.ControllerFamily
        family.API().ReadXml(p_controller_obj, p_xml)
        # try:
        #    l_xml = self.m_pyhouse_obj.House.OBJs.FamilyData[l_family].FamilyXmlModuleName
        #    l_xml().ReadXml(p_controller_obj, p_xml)
        # except Exception as e_err:  # ControllerFamily invalid or missing
        #    LOG.error('ERROR - Read Family Data {0:}'.format(e_err))

    def _read_interface_data(self, p_obj, p_xml):
        try:
            interface.ReadWriteConfigXml().read_interface_xml(p_obj, p_xml)
        except Exception as e_err:  # ControllerFamily invalid or missing
            LOG.error('ERROR - Read Interface Data - {0:} - {1:} - {2:}'.format(e_err, p_obj.Name, p_obj.InterfaceType))

    def read_one_controller_xml(self, p_controller_xml):
        try:
            l_controller_obj = self._read_controller_data(p_controller_xml)
            l_controller_obj.Key = self.m_count  # Renumber
            self._read_family_data(l_controller_obj, p_controller_xml)
            self._read_interface_data(l_controller_obj, p_controller_xml)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneController - {0:}'.format(e_err))
        return l_controller_obj

    def read_controllers_xml(self, p_controller_sect_xml):
        """Called from lighting.
        """
        self.m_count = 0
        l_dict = {}
        # PrettyPrintAny(l_controllers_xml, 'Lighting Controllers')
        try:
            for l_controller_xml in p_controller_sect_xml.iterfind('Controller'):
                l_controller_obj = self.read_one_controller_xml(l_controller_xml)
                l_dict[self.m_count] = l_controller_obj
                self.m_count += 1
        except AttributeError as e_error:  # No Controller section
            LOG.warning('Lighting Controllers - No Controllers found - {0:}'.format(e_error))
            l_dict = {}
        return l_dict


    def _write_controller_data(self, p_obj, p_xml):
        self.put_text_element(p_xml, 'InterfaceType', p_obj.InterfaceType)
        self.put_text_element(p_xml, 'Port', p_obj.Port)

    def _write_family_data(self, p_controller_obj, p_xml):
        l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_controller_obj.ControllerFamily].FamilyModuleAPI
        l_api.insert_device_xml(p_xml, p_controller_obj)

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
