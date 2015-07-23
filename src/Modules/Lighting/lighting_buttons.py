"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting_buttons -*-

@name:      PyHouse/src/Modules/Lighting/lighting_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import ButtonData
from Modules.Lighting.lighting_core import API as LightingCoreAPI
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logging
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools

LOG = Logging.getLogger('PyHouse.LightingButton ')


class API(object):

    @staticmethod
    def _read_button_data(p_xml, p_version):
        l_obj = ButtonData()
        l_obj = LightingCoreAPI.read_core_lighting_xml(l_obj, p_xml, p_version)
        l_obj.DeviceSubType = 3
        return l_obj

    @staticmethod
    def _read_family_data(p_pyhouse_obj, p_obj, p_xml):
        l_api = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    @staticmethod
    def read_one_button_xml(p_pyhouse_obj, p_button_xml, p_version):
        l_button_obj = API._read_button_data(p_button_xml, p_version)
        API._read_family_data(p_pyhouse_obj, l_button_obj, p_button_xml)
        l_button_obj.DeviceType = 1
        l_button_obj.DeviceSubType = 3
        return l_button_obj

    @staticmethod
    def read_all_buttons_xml(p_pyhouse_obj, p_button_sect_xml, p_version):
        l_count = 0
        l_button_dict = {}
        try:
            for l_button_xml in p_button_sect_xml.iterfind('Button'):
                l_obj = API.read_one_button_xml(p_pyhouse_obj, l_button_xml, p_version)
                l_obj.Key = l_count  # Renumber
                l_button_dict[l_count] = l_obj
                l_count += 1
        except AttributeError as e_error:  # No Buttons
            LOG.warning('No Buttons defined - {0:}'.format(e_error))
            l_button_dict = {}
        LOG.info("Loaded {} buttons".format(l_count))
        return l_button_dict


    @staticmethod
    def _write_family_data(p_pyhouse_obj, p_button_obj, p_xml):
        try:
            l_family = p_button_obj.DeviceFamily
            l_family_obj = p_pyhouse_obj.House.RefOBJs.FamilyData[l_family]
            l_api = l_family_obj.FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_button_obj)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

    @staticmethod
    def write_one_button_xml(p_pyhouse_obj, p_button_obj):
        l_button_xml = LightingCoreAPI.write_base_lighting_xml('Button', p_button_obj)
        API._write_family_data(p_pyhouse_obj, p_button_obj, l_button_xml)
        return l_button_xml

    @staticmethod
    def write_buttons_xml(p_pyhouse_obj):
        l_count = 0
        l_buttons_xml = ET.Element('ButtonSection')
        for l_button_obj in p_pyhouse_obj.House.DeviceOBJs.Buttons.itervalues():
            l_entry = API.write_one_button_xml(p_pyhouse_obj, l_button_obj)
            l_buttons_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Buttons XML'.format(l_count))
        return l_buttons_xml

# ## END DBK
