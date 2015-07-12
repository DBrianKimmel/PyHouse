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
from Modules.Lighting.lighting_core import LightingCoreXmlAPI
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logging
from Modules.Utilities.xml_tools import PutGetXML

LOG = Logging.getLogger('PyHouse.LightgLights   ')
SECTION = 'LightSection'


class LLApi(LightingCoreXmlAPI):
    """
    Get/Put all the information about one light:
        Base Light Data
        Light Data
        Family Data
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    @staticmethod
    def _read_light_data(p_xml):
        l_light_obj = LightData()
        l_light_obj = LightingCoreXmlAPI().read_core_lighting_xml(l_light_obj, p_xml)
        l_light_obj.DeviceSubType = 2
        l_light_obj.CurLevel = PutGetXML.get_int_from_xml(p_xml, 'CurLevel', 0)
        return l_light_obj

    def _read_family_data(self, p_obj, p_xml):
        l_api = FamUtil.read_family_data(self.m_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    def _read_one_light_xml(self, p_light_xml):
        l_light_obj = LLApi._read_light_data(p_light_xml)
        l_light_obj.Key = 0
        self._read_family_data(l_light_obj, p_light_xml)
        l_light_obj.DeviceType = 1
        l_light_obj.DeviceSubType = 2
        return l_light_obj

    def read_all_lights_xml(self, p_light_sect_xml):
        """
        @param p_light_sect_xml: the "LightSection" of the config
        """
        l_count = 0
        l_lights_dict = {}
        try:
            for l_light_xml in p_light_sect_xml.iterfind('Light'):
                l_light = self._read_one_light_xml(l_light_xml)
                l_light.Key = l_count  # Renumber
                l_lights_dict[l_count] = l_light
                l_count += 1
        except AttributeError as e_error:  # No Lights section
            LOG.warning('Lighting_Lights - No Lights defined - {0:}'.format(e_error))
            l_lights_dict = {}
        LOG.info("Loaded {} Lights".format(l_count))
        return l_lights_dict


    def _write_light_data(self, p_light_obj, l_light_xml):
        PutGetXML.put_text_element(l_light_xml, 'LightingType', p_light_obj.LightingType)
        PutGetXML.put_text_element(l_light_xml, 'CurLevel', p_light_obj.CurLevel)

    def _add_family_data(self, p_light_obj, p_xml):
        """
        Add the family specific information of the device to the XML.
        """
        try:
            l_device_family = p_light_obj.DeviceFamily
            l_family_obj = self.m_pyhouse_obj.House.RefOBJs.FamilyData[l_device_family]
            l_api = l_family_obj.FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_light_obj)
        except Exception as e_err:
            LOG.error('Family:{}\n\t{}'.format(l_device_family, e_err))

    def write_one_light_xml(self, p_light_obj):
        l_light_xml = self.write_base_lighting_xml('Light', p_light_obj)
        self._write_light_data(p_light_obj, l_light_xml)
        self._add_family_data(p_light_obj, l_light_xml)
        return l_light_xml

    def write_all_lights_xml(self, p_lights_obj):
        l_xml = ET.Element(SECTION)
        l_count = 0
        for l_light_obj in p_lights_obj.itervalues():
            l_xml.append(self.write_one_light_xml(l_light_obj))
            l_count += 1
        LOG.info('Saved XML')
        return l_xml

# ## END DBK
