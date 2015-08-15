"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 27, 2013
@summary:   This module is for testing Insteon conversion routines.

Passed all 3 tests - DBL - 2015-08-15

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Families.Insteon import Insteon_utils
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG

ADDR_DR_SLAVE_MSG = bytearray(b'\x16\xc9\xd0')
ADDR_DR_SLAVE_INT = 1493456
ADDR_NOOK_MSG = bytearray(b'\x17\xc2\x72')
ADDR_NOOK_INT = 1557106

MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.inst = Insteon_utils.Util


class C02_Conversions(SetupMixin, unittest.TestCase):


    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.inst = Insteon_utils.Util

    def test_01_Message2int(self):
        result = self.inst.message2int(MSG_50, 2)
        self.assertEqual(result, ADDR_DR_SLAVE_INT)
        result = self.inst.message2int(MSG_62, 2)
        self.assertEqual(result, ADDR_NOOK_INT)

    def test_02_Int2message(self):
        l_msg = MSG_50
        result = self.inst.int2message(ADDR_DR_SLAVE_INT, l_msg, 2)
        self.assertEqual(result[2:5], ADDR_DR_SLAVE_MSG)
        l_msg = MSG_62
        result = self.inst.int2message(ADDR_NOOK_INT, l_msg, 2)
        self.assertEqual(result[2:5], ADDR_NOOK_MSG)

    def test_03_Json(self):
        pass

# ## END DBK
