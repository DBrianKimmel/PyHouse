"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting_controllers -*-

@name:      PyHouse/src/Modules/Lighting/lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.


Note that controllers have common light info and also have controller info,
family info, and interface info.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Lighting.lighting_core import LightingCoreXmlAPI
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger
from Modules.Drivers.interface import Xml as interfaceXML
from Modules.Utilities.xml_tools import PutGetXML

LOG = Logger.getLogger('PyHouse.Controller     ')


class LCApi(LightingCoreXmlAPI):
    """
    Get/Put all the information about one controller:
        Base Light Data
        Controller Data
        Family Data
        Interface Data
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _read_base_data(self, p_xml):
        """
        @return: a Controller data object with the base info filled in
        """
        LOG.info('')
        l_obj = ControllerData()  # Create an empty controller object.
        l_obj = self.read_core_lighting_xml(l_obj, p_xml)
        l_obj.DeviceSubType = 1
        return l_obj

    def _read_controller_data(self, p_obj, p_xml):
        """
        There are 2 extra fields for controllers - get them.
        """
        LOG.info('Name:{}; Family:{}'.format(p_obj.Name, p_obj.DeviceFamily))
        p_obj.InterfaceType = PutGetXML.get_text_from_xml(p_xml, 'InterfaceType')
        p_obj.Port = PutGetXML.get_text_from_xml(p_xml, 'Port')
        return p_obj

    def _read_interface_data(self, p_obj, p_xml):
        LOG.info('Name:{}; Family:{}'.format(p_obj.Name, p_obj.DeviceFamily))
        try:
            interfaceXML.read_interface_xml(p_obj, p_xml)
        except Exception as e_err:  # DeviceFamily invalid or missing
            LOG.error('ERROR - Read Interface Data - {} - {} - {}'.format(e_err, p_obj.Name, p_obj.InterfaceType))
        return p_obj

    def _read_family_data(self, p_obj, p_xml):
        LOG.info('Name:{}; Family:{}'.format(p_obj.Name, p_obj.DeviceFamily))
        l_api = FamUtil.read_family_data(self.m_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    def read_one_controller_xml(self, p_xml):
        LOG.info('')
        try:
            l_obj = self._read_base_data(p_xml)
            self._read_controller_data(l_obj, p_xml)
            self._read_interface_data(l_obj, p_xml)
            self._read_family_data(l_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneController - {0:}'.format(e_err))
            l_obj = ControllerData()
        l_obj.DeviceType = 1
        l_obj.DeviceSubType = 1
        return l_obj

    def read_all_controllers_xml(self, p_controller_sect_xml):
        """Called from lighting.

        @param p_controller_section_xml: is the XML element containing all controllers. <ControllerSection>
        """
        l_count = 0
        l_dict = {}
        try:
            for l_controller_xml in p_controller_sect_xml.iterfind('Controller'):
                l_controller_obj = self.read_one_controller_xml(l_controller_xml)
                l_controller_obj.Key = l_count
                l_dict[l_count] = l_controller_obj
                l_count += 1
        except AttributeError as e_error:  # No Controller section
            LOG.warning('No Controllers found - {}'.format(e_error))
        LOG.info("Loaded {} Controllers".format(l_count))
        return l_dict


    def _write_base_data(self, p_obj):
        l_xml = self.write_base_lighting_xml('Controller', p_obj)
        return l_xml

    def _write_controller_data(self, p_obj, p_xml):
        PutGetXML.put_text_element(p_xml, 'InterfaceType', p_obj.InterfaceType)
        PutGetXML.put_text_element(p_xml, 'Port', p_obj.Port)

    def _write_family_data(self, p_controller_obj, p_xml):
        try:
            l_family = p_controller_obj.DeviceFamily
            l_family_obj = self.m_pyhouse_obj.House.RefOBJs.FamilyData[l_family]
            l_api = l_family_obj.FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_controller_obj)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

    def _write_interface_data(self, p_obj, p_xml):
        interfaceXML.write_interface_xml(p_obj, p_xml)

    def write_one_controller_xml(self, p_controller_obj):
        l_controller_xml = self.write_base_lighting_xml('Controller', p_controller_obj)
        self._write_controller_data(p_controller_obj, l_controller_xml)
        self._write_family_data(p_controller_obj, l_controller_xml)
        self._write_interface_data(p_controller_obj, l_controller_xml)
        return l_controller_xml

    def write_all_controllers_xml(self, p_controller_sect_obj):
        l_count = 0
        l_controllers_xml = ET.Element('ControllerSection')
        for l_controller_obj in p_controller_sect_obj.itervalues():
            l_controllers_xml.append(self.write_one_controller_xml(l_controller_obj))
            l_count += 1
        LOG.info('Saved XML')
        return l_controllers_xml

# ## END DBK
