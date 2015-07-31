"""
-*- test-case-name: PyHouse.src.Modules.lights.test.test_lighting_lights -*-

@name:      PyHouse/src/Modules/lights/lighting_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2015 by D. Brian Kimmel
@note:      Created on May 1, 2011
@license:   MIT License
@summary:   This module handles the lights component of the lighting system.

Inherit from lighting_core.

Each entry should contain enough information to allow functionality of various family of lighting controllers.

Insteon is the first type coded and UPB is to follow.

The real work of controlling the devices is delegated to the modules for that family of devices.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import LightData
from Modules.Lighting.lighting_core import API as LightingCoreAPI
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logging
from Modules.Utilities.xml_tools import PutGetXML

LOG = Logging.getLogger('PyHouse.LightgLights   ')
SECTION = 'LightSection'


class Utility(object):

    @staticmethod
    def _read_base_device(p_xml, p_version):
        """
        @param p_xml: is the XML Element for the entire device
        @param p_version: is some helper data to get the correct information from the config file.
        @return: a Light data object with the base info filled in
        """
        l_obj = LightData()
        l_obj = LightingCoreAPI.read_core_lighting_xml(l_obj, p_xml, p_version)
        l_obj.DeviceType = 1
        l_obj.DeviceSubType = 2
        return l_obj

    @staticmethod
    def _write_base_device(p_pyhouse_obj, p_light_obj):
        l_xml = LightingCoreAPI.write_core_lighting_xml('Light', p_light_obj)
        return l_xml


    @staticmethod
    def _read_light_data(p_obj, p_xml, p_version):
        p_obj.CurLevel = PutGetXML.get_int_from_xml(p_xml, 'CurLevel', 0)
        p_obj.IsDimmable = PutGetXML.get_bool_from_xml(p_xml, 'IsDimmable', False)
        return p_obj  # for testing

    @staticmethod
    def _write_light_data(p_obj, p_xml):
        PutGetXML.put_text_element(p_xml, 'CurLevel', p_obj.CurLevel)
        PutGetXML.put_text_element(p_xml, 'IsDimmable', p_obj.IsDimmable)
        return p_xml


    @staticmethod
    def _read_family_data(p_pyhouse_obj, p_obj, p_xml, p_version):
        l_api = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    @staticmethod
    def _write_family_data(p_pyhouse_obj, p_obj, p_xml):
        try:
            l_family = p_obj.DeviceFamily
            l_family_obj = p_pyhouse_obj.House.RefOBJs.FamilyData[l_family]
            l_api = l_family_obj.FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_obj)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))


    @staticmethod
    def _read_one_light_xml(p_pyhouse_obj, p_xml, p_version):
        """
        Load all the xml for one controller.
        Base Device, Light, Family
        """
        try:
            l_obj = Utility._read_base_device(p_xml, p_version)
            Utility._read_light_data(l_obj, p_xml, p_version)
            Utility._read_family_data(p_pyhouse_obj, l_obj, p_xml, p_version)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneController - {0:}'.format(e_err))
            l_obj = LightData()
        return l_obj

    @staticmethod
    def _write_one_light_xml(p_pyhouse_obj, p_controller_obj):
        l_xml = Utility._write_base_device(p_pyhouse_obj, p_controller_obj)
        Utility._write_light_data(p_controller_obj, l_xml)
        Utility._write_family_data(p_pyhouse_obj, p_controller_obj, l_xml)
        return l_xml


class API(object):

    @staticmethod
    def read_all_lights_xml(p_pyhouse_obj, p_light_sect_xml, p_version):
        """
        @param p_pyhouse_obj: is the master information store
        @param p_light_sect_xml: the "LightSection" of the config
        @param p_version: is the XML version of the file to use.
        @return: a dict of lights info
        """
        l_count = 0
        l_dict = {}
        try:
            for l_xml in p_light_sect_xml.iterfind('Light'):
                l_light = Utility._read_one_light_xml(p_pyhouse_obj, l_xml, p_version)
                l_light.Key = l_count  # Renumber
                l_dict[l_count] = l_light
                l_count += 1
        except AttributeError as e_err:  # No Lights section
            LOG.warning('Lighting_Lights - No Lights defined - {}'.format(e_err))
            # print('XXX-1', e_err)
            l_dict = {}
        LOG.info("Loaded {} Lights".format(l_count))
        return l_dict


    @staticmethod
    def write_all_lights_xml(p_pyhouse_obj):
        l_xml = ET.Element(SECTION)
        l_count = 0
        for l_light_obj in p_pyhouse_obj.House.DeviceOBJs.Lights.itervalues():
            l_xml.append(API.write_one_light_xml(p_pyhouse_obj, l_light_obj))
            l_count += 1
        LOG.info('Saved {} Lights XML'.format(l_count))
        return l_xml

# ## END DBK
