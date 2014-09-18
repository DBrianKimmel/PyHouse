"""
-*- test-case-name: PyHouse.src.Modules.families.Insteon.test.test_Insteon_PLM -*-

@name: PyHouse/src/Modules/families/Insteon/Insteon_PLM.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 8, 2013
@license: MIT License
@summary: This module is for driving serial devices


"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
# from Modules.lights.lighting import LightData
from Modules.Core.data_objects import PyHouseData, ControllerData
from Modules.Families.Insteon import Insteon_PLM
from Modules.Core import conversions
from Modules.Families import family
# from Modules.Utilities.tools import PrettyPrintAny
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


ADR_16C9D0 = '16.C9.D0'
ADR_17C272 = '17.C2.72'
BA_17C272 = bytearray(b'\x17\xc2\x72')
BA_1B4781 = bytearray(b'\x1b\x47\x81')
MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')
MSG_99 = bytearray(b'\x02\x99')
MT_12345 = bytearray(b'\x02\x50\x14\x93\x6f\xaa\xaa\xaa\x07\x6e\x4f')
STX = 0x02


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()


class Test_01_InsteonPlmUtility(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = Insteon_PLM.API()

    def test_0101_MessageLength(self):
        self.assertEqual(self.m_api._get_message_length(MSG_50), 11)
        self.assertEqual(self.m_api._get_message_length(MSG_62), 9)
        self.assertEqual(self.m_api._get_message_length(MSG_99), 1)

    def test_0102_ExtractAddress(self):
        # self.assertEqual(self.m_api._get_addr_from_message(MSG_50, 2), conversions.dotted_hex2int(ADR_16C9D0))
        # self.assertEqual(self.m_api._get_addr_from_message(MSG_62, 2), conversions.dotted_hex2int(ADR_17C272))
        pass

    def test_0103_QueueCommand(self):
        l_ret_1 = self.m_api._queue_command('insteon_send')
        self.assertEqual(len(l_ret_1), 8)
        self.assertEqual(l_ret_1[0], STX)


class Test_02_CreateCommands(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_api = Insteon_PLM. API()
        pass

    def test_0201_get_message_length(self):
        self.assertEqual(self.m_api._get_message_length(MSG_50), 11)
        self.assertEqual(self.m_api._get_message_length(MSG_62), 9)
        self.assertEqual(self.m_api._get_message_length(MSG_99), 1)

    def test_0201_getBytes(self):
        pass


class Test_03_PlmDriverProtocol(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_api = Insteon_PLM. API()


class Test_55_Thermostat(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_controller_obj = ControllerData()

    def test_0301_x(self):
        pass

# ## END DBK
