"""
-*- test-case-name: PyHouse.src.Modules.families.Insteon.test.test_Insteon_PLM -*-

@name: PyHouse/src/Modules/families/Insteon/Insteon_PLM.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
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
from Modules.families.Insteon import Insteon_PLM
from Modules.families.Insteon import Insteon_utils
from Modules.families import family
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data, test_mixin


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

    def setUp(self):
        test_mixin.Setup()
        test_mixin.Setup().BuildPyHouse()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = Insteon_PLM.API()


class Test_01(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

    def test_0101_MessageLength(self):
        self.assertEqual(self.m_api._get_message_length(MSG_50), 11)
        self.assertEqual(self.m_api._get_message_length(MSG_62), 9)
        self.assertEqual(self.m_api._get_message_length(MSG_99), 1)

    def test_0102_ExtractAddress(self):
        self.assertEqual(self.m_api._get_addr_from_message(MSG_50, 2), Insteon_utils.dotted_3hex2int(ADR_16C9D0))
        self.assertEqual(self.m_api._get_addr_from_message(MSG_62, 2), Insteon_utils.dotted_3hex2int(ADR_17C272))

    def test_0103_QueueCommand(self):
        l_ret_1 = self.m_api._queue_command('insteon_send')
        self.assertEqual(len(l_ret_1), 8)
        self.assertEqual(l_ret_1[0], STX)


class Test_02(SetupMixin, unittest.TestCase):

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


class Test_03_Thermostat(SetupMixin, unittest.TestCase):

    def setUp(self):
        # super(Test_03_Thermostat, self).__init__()
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)
        self.m_controller_obj = ControllerData()

    def test_0301_x(self):
        self.m_api._decode_50_record(self.m_controller_obj)
        PrettyPrintAny(self.m_controller_obj, 'controller_obj', 120)

# ## END DBK
