"""
@name:      PyHouse/src/Modules/Utilities/test_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2015 by D. Brian Kimmel
@note:      Created on Apr 11, 2013
@license:   MIT License
@summary:   Various functions and utility methods.

Passed all 13 tests - DBK - 2015-08-05

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.setup_logging import LOGGING_DICT
from Modules.Utilities.obj_defs import GetPyhouse
from Modules.Utilities import tools
from Modules.Lighting.lighting_lights import API as lightsAPI
from Modules.Families.family import API as familyAPI
from Modules.Computer import logging_pyh as Logger
from test.xml_data import XML_LONG, XML_EMPTY
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_version = '1.4.0'


class A_PB1(SetupMixin, unittest.TestCase):
    """Test PrintBytes functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_String(self):
        """Testing PrintBytes.
        """
        l_str = bytearray('1234')
        l_str[0] = 0x00
        l_str[1] = 0x7f
        l_str[2] = 0x80
        l_str[3] = 0xff
        l_ans = tools.PrintBytes(l_str)
        self.assertEqual(l_ans, ' 0x00 0x7f 0x80 0xff <END>')


class C1_Find(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = GetPyhouse(self.m_pyhouse_obj)
        self.m_light_api = lightsAPI()
        self.m_pyhouse_obj.House.FamilyData = familyAPI(self.m_pyhouse_obj).m_family
        self.m_pyhouse_obj.House.Lights = self.m_light_api.read_all_lights_xml(self.m_pyhouse_obj, self.m_xml.light_sect, self.m_version)

    def test_01_Setup(self):
        l_loc = self.m_api.Location().Latitude
        # print(l_loc)

# ## END DBK
