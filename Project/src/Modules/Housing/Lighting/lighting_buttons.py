"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting_buttons -*-

@name:      PyHouse/src/Modules/Lighting/lighting_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

"""

__updated__ = '2019-01-23'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyHouse files
from Modules.Core.data_objects import ButtonData
# from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.Core.Utilities.xml_tools import XmlConfigTools
# from Modules.Families.family_utils import FamUtil
from Modules.Housing.Lighting.lighting_xml import LightingXML

from Modules.Computer import logging_pyh as Logging
LOG = Logging.getLogger('PyHouse.LightingButton ')

""" Data

    x_pyhouse_obj.House.Lighting.Buttons.
                    BaseUUIDObject
                    DeviceObject
"""


class XML:

    def _read_one_button_xml(self, p_pyhouse_obj, p_button_xml):
        l_obj = ButtonData()
        l_obj.DeviceType = 1  # Lighting
        l_obj.DeviceSubType = 1  # Button
        l_button_obj = LightingXML()._read_base_device(l_obj, p_button_xml)
        LightingXML()._read_family_data(p_pyhouse_obj, l_button_obj, p_button_xml)
        return l_button_obj

    def _write_one_button_xml(self, p_pyhouse_obj, p_button_obj):
        l_button_xml = LightingXML()._write_base_device('Button', p_button_obj)
        LightingXML()._write_family_data(p_pyhouse_obj, p_button_obj, l_button_xml)
        return l_button_xml

    def read_all_buttons_xml(self, p_pyhouse_obj):
        l_count = 0
        l_dict = {}
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/LightingSection/ButtonSection')
        if l_xml is None:
            return l_dict
        try:
            for l_button_xml in l_xml.iterfind('Button'):
                l_obj = self._read_one_button_xml(p_pyhouse_obj, l_button_xml)
                l_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_obj
                LOG.info('Loaded button {}'.format(l_obj.Name))
                l_count += 1
        except AttributeError as e_error:  # No Buttons
            LOG.warning('No Buttons defined - {}'.format(e_error))
            l_dict = {}
        LOG.info("Loaded {} buttons".format(l_count))
        return l_dict

    def write_all_buttons_xml(self, p_pyhouse_obj):
        l_count = 0
        l_buttons_xml = ET.Element('ButtonSection')
        for l_button_obj in p_pyhouse_obj.House.Lighting.Buttons.values():
            l_entry = self._write_one_button_xml(p_pyhouse_obj, l_button_obj)
            l_buttons_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Buttons XML'.format(l_count))
        return l_buttons_xml

#  ## END DBK
