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
from Modules.Lighting.lighting_core import LightingCoreXmlAPI
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logging
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools

LOG = Logging.getLogger('PyHouse.LightgButton')


class LBApi(LightingCoreXmlAPI):

    m_count = 0

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _read_button_data(self, p_xml):
        l_obj = ButtonData()
        l_obj = self.read_core_lighting_xml(l_obj, p_xml)
        l_obj.DeviceSubType = 3
        return l_obj

    def _read_family_data(self, p_obj, p_xml):
        l_api = FamUtil.read_family_data(self.m_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    def read_one_button_xml(self, p_button_xml):
        l_button_obj = self._read_button_data(p_button_xml)
        self._read_family_data(l_button_obj, p_button_xml)
        l_button_obj.Key = self.m_count  # Renumber
        l_button_obj.DeviceType = 1
        l_button_obj.DeviceSubType = 3
        return l_button_obj

    def read_all_buttons_xml(self, p_button_sect_xml):
        self.m_count = 0
        l_button_dict = {}
        try:
            for l_button_xml in p_button_sect_xml.iterfind('Button'):
                l_button_dict[self.m_count] = self.read_one_button_xml(l_button_xml)
                self.m_count += 1
        except AttributeError as e_error:  # No Buttons
            LOG.warning('No Buttons defined - {0:}'.format(e_error))
            l_button_dict = {}
        LOG.info("Loaded {} buttons".format(self.m_count))
        return l_button_dict


    def write_one_button_xml(self, p_button_obj):
        l_button_xml = self.write_base_lighting_xml('Button', p_button_obj)
        self._add_family_data(p_button_obj, l_button_xml)
        return l_button_xml

    def write_buttons_xml(self, p_buttons_obj):
        self.m_count = 0
        l_buttons_xml = ET.Element('ButtonSection')
        for l_button_obj in p_buttons_obj.itervalues():
            l_entry = self.write_one_button_xml(l_button_obj)
            l_buttons_xml.append(l_entry)
            self.m_count += 1
        return l_buttons_xml

# ## END DBK
