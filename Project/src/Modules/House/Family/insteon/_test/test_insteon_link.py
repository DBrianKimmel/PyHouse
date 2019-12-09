"""
@name:      PyHouse/src/Modules/Families/Insteon/_test/test_Insteon_Link.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 16, 2015
@Summary:

"""

__updated__ = '2019-10-15'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerInformation
from Modules.House.Family.insteon.Insteon_Link import DecodeLink as linkDecode
# from Modules.Families.Insteon.Insteon_utils import Decode
from _test.testing_mixin import SetupPyHouseObj
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny, FormatBytes

MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_53 = bytearray(b'\x02\x53\x00\x01\x12\x34\x56\x02\x04\x06\xFF')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_obj = ControllerInformation()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Insteon_Link')


class B01_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_53_Decode(self):
        self.m_obj._Message = MSG_53
        # print(FormatBytes(self.m_obj._Message))
        # print(PrettyFormatAny.form(self.m_obj._Message, 'B01-53-A - Obj'))
        _l_ret = linkDecode.decode_53(self.m_obj)

# ## END DBK
