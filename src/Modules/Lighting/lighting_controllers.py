"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting_controllers -*-

@name:      PyHouse/src/Modules/Lighting/lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

Note that controllers have common light info and also have controller info, family info, and interface info.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Lighting.lighting_core import API as LightingCoreAPI
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger
from Modules.Drivers.interface import Xml as interfaceXML
from Modules.Utilities.xml_tools import PutGetXML
from Modules.Utilities import debug_tools

LOG = Logger.getLogger('PyHouse.LightController')


class Utility(object):

    @staticmethod
    def _read_base_device(p_xml, p_version):
        """
        @param p_xml: is the XML Element for the entire device
        @param p_version: is some helper data to get the correct information from the config file.
        @return: a Controller data object with the base info filled in
        """
        l_obj = ControllerData()  # Create an empty controller object.
        l_obj = LightingCoreAPI.read_core_lighting_xml(l_obj, p_xml, p_version)
        # l_obj.DeviceSubType = 1
        return l_obj

    @staticmethod
    def _write_base_device(p_obj):
        l_xml = LightingCoreAPI.write_core_lighting_xml('Controller', p_obj)
        return l_xml


    @staticmethod
    def _read_controller_data(p_obj, p_xml, p_version):
        """
        There are extra fields for controllers - get them.
        See ControllerData()
        """
        p_obj.InterfaceType = PutGetXML.get_text_from_xml(p_xml, 'InterfaceType')
        p_obj.Port = PutGetXML.get_text_from_xml(p_xml, 'Port')
        return p_obj  # for testing

    @staticmethod
    def _write_controller_data(p_obj, p_xml):
        PutGetXML.put_text_element(p_xml, 'InterfaceType', p_obj.InterfaceType)
        PutGetXML.put_text_element(p_xml, 'Port', p_obj.Port)
        return p_xml


    @staticmethod
    def _read_interface_data(p_obj, p_xml, _p_version):
        try:
            interfaceXML.read_interface_xml(p_obj, p_xml)
        except Exception as e_err:  # DeviceFamily invalid or missing
            LOG.error('ERROR - Read Interface Data - {} - {} - {}'.format(e_err, p_obj.Name, p_obj.InterfaceType))
        return p_obj

    @staticmethod
    def _write_interface_data(p_obj, p_xml):
        try:
            interfaceXML.write_interface_xml(p_obj, p_xml)
        except Exception:
            pass
        return p_xml


    @staticmethod
    def _read_family_data(p_pyhouse_obj, p_obj, p_xml, _p_version):
        """Read the family specific data for this controller.
        """
        # l_debug = debug_tools._format_object('Obj', p_obj, 100)
        # print('Read controller {}'.format(l_debug))
        l_api = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    @staticmethod
    def _write_family_data(p_pyhouse_obj, p_controller_obj, p_xml):
        try:
            l_family = p_controller_obj.DeviceFamily
            l_family_obj = p_pyhouse_obj.House.FamilyData[l_family]
            l_api = l_family_obj.FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_controller_obj)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

    @staticmethod
    def _read_one_controller_xml(p_pyhouse_obj, p_xml, p_version):
        """
        Load all the xml for one controller.
        Base Device, Controller, Family and Interface
        """
        try:
            l_obj = Utility._read_base_device(p_xml, p_version)
            Utility._read_controller_data(l_obj, p_xml, p_version)
            Utility._read_interface_data(l_obj, p_xml, p_version)
            Utility._read_family_data(p_pyhouse_obj, l_obj, p_xml, p_version)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneController - {0:}'.format(e_err))
            l_obj = ControllerData()
        return l_obj

    @staticmethod
    def _write_one_controller_xml(p_pyhouse_obj, p_controller_obj):
        l_controller_xml = Utility._write_base_device(p_controller_obj)
        Utility._write_controller_data(p_controller_obj, l_controller_xml)
        Utility._write_interface_data(p_controller_obj, l_controller_xml)
        Utility._write_family_data(p_pyhouse_obj, p_controller_obj, l_controller_xml)
        return l_controller_xml


class API(object):

    @staticmethod
    def read_all_controllers_xml(p_pyhouse_obj, p_controller_sect_xml, p_version):
        """Called from lighting.
        Get the entire configuration of all the controllers and place them in a holding dict.

        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_controller_section_xml: is the XML element containing all controllers. <ControllerSection>
        @param p_version: is the old version of the XML Config file
        @return: a dict of all the controllers configured.
        """
        l_count = 0
        l_dict = {}
        try:
            for l_controller_xml in p_controller_sect_xml.iterfind('Controller'):
                l_controller_obj = Utility._read_one_controller_xml(p_pyhouse_obj, l_controller_xml, p_version)
                l_controller_obj.Key = l_count
                l_dict[l_count] = l_controller_obj
                l_count += 1
        except AttributeError as e_error:  # No Controller section
            LOG.warning('No Controllers found - {}'.format(e_error))
        LOG.info("Loaded {} Controllers".format(l_count))
        return l_dict


    @staticmethod
    def write_all_controllers_xml(p_pyhouse_obj):
        l_count = 0
        l_controllers_xml = ET.Element('ControllerSection')
        for l_controller_obj in p_pyhouse_obj.House.Controllers.itervalues():
            l_controllers_xml.append(Utility._write_one_controller_xml(p_pyhouse_obj, l_controller_obj))
            l_count += 1
        LOG.info('Saved {} Controllers XML'.format(l_count))
        return l_controllers_xml

# ## END DBK
