"""
-*- test-case-name: PyHouse.src.Modules.lights.test.test_lighting_lights -*-

@name: PyHouse/src/Modules/lights/lighting_lights.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on May 1, 2011
@license: MIT License
@summary: This module handles the lights component of the lighting system.

Inherit from lighting_core.

Each entry should contain enough information to allow functionality of various family of lighting controllers.

Insteon is the first type coded and UPB is to follow.

The real work of controlling the devices is delegated to the modules for that family of devices.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import LightData
from Modules.lights.lighting_core import ReadWriteConfigXml
from Modules.utils import pyh_log
from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.LightgLights')


class LightingLightsAPI(ReadWriteConfigXml):
    """
    Get/Put all the information about one light:
        Base Light Data
        Light Data
        Family Data
    """

    m_count = 0

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _read_light_data(self, p_xml):
        l_light_obj = LightData()
        l_light_obj = self.read_base_lighting_xml(l_light_obj, p_xml)
        l_light_obj.IsController = self.get_text_from_xml(p_xml, 'IsController')
        l_light_obj.CurLevel = self.get_int_from_xml(p_xml, 'CurLevel', 0)
        return l_light_obj

    def _read_family_data(self, p_obj, p_xml):
        l_api = None
        try:
            l_family = p_obj.ControllerFamily
            l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[l_family].FamilyModuleAPI
            print('API = {0:}'.format(l_api))
            l_api.ReadXml(p_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR in reading family Data {0:}'.format(e_err))
            print('ERROR in reading family Data {0:}'.format(e_err))
        return l_api  # for testing

    def read_one_light_xml(self, p_light_xml):
        l_light_obj = self._read_light_data(p_light_xml)
        print('Light {0:}'.format(l_light_obj))
        l_light_obj.Key = self.m_count  # Renumber
        self._read_family_data(l_light_obj, p_light_xml)
        return l_light_obj

    def read_all_lights_xml(self, p_light_sect_xml):
        self.m_count = 0
        l_lights_dict = {}
        try:
            for l_light_xml in p_light_sect_xml.iterfind('Light'):
                l_lights_dict[self.m_count] = self.read_one_light_xml(l_light_xml)
                self.m_count += 1
        except AttributeError as e_error:  # No Lights section
            LOG.warning('Lighting_Lights - No Lights defined - {0:}'.format(e_error))
            l_lights_dict = {}
        return l_lights_dict


    def _write_light_data(self, p_light_obj, l_light_xml):
        self.put_text_element(l_light_xml, 'IsController', p_light_obj.IsController)
        # self.put_text_element(l_light_xml, 'LightingType', p_light_obj.LightingType)
        self.put_text_element(l_light_xml, 'CurLevel', p_light_obj.CurLevel)
        pass

    def _write_family_data(self, p_light_obj, p_light_xml):
        l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_light_obj.ControllerFamily].FamilyModuleAPI
        l_api.insert_device_xml(p_light_xml, p_light_obj)

    def write_one_light_xml(self, p_light_obj):
        l_light_xml = self.write_base_lighting_xml(p_light_obj)
        self._write_light_data(p_light_obj, l_light_xml)
        self._write_family_data(p_light_obj, l_light_xml)
        self
        return l_light_xml

    def write_all_lights_xml(self, p_lights_obj):
        l_xml = ET.Element('LightSection')
        self.m_count = 0
        for l_light_obj in p_lights_obj.itervalues():
            l_xml.append(self.write_one_light_xml(l_light_obj))
            self.m_count += 1
        return l_xml

# ## END DBK
