"""
-*- test-case-name: PyHouse.Modules.Core.test.test_node_local -*-

@name:      PyHouse/src/Modules/Core/node_local.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test the UPB controller.

"""

# Import system type stuff
from twisted.trial import unittest
import Queue

# Import PyMh files and modules.
from Modules.Families.UPB import UPB_Pim
from Modules.Core.data_objects import ControllerData
from Modules.Utilities.tools import PrintBytes  # , PrettyPrintAny

CHG_REG_CMD = b'\x70\x03'


class Test_01_Utils(unittest.TestCase):

    def setUp(self):
        self.m_api = UPB_Pim.BuildCommand()
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Queue = Queue.Queue(300)

    def test_0101_Nibble2Hex(self):
        l_hex = self.m_api._nibble_to_hex(0x00)
        self.assertEqual(l_hex, 0x30)
        print('test_0101/  0x00 ==> {0:#2x} '.format(l_hex), l_hex)
        #
        l_hex = self.m_api._nibble_to_hex(0x07)
        self.assertEqual(l_hex, 0x37)
        #
        l_hex = self.m_api._nibble_to_hex(0x0A)
        self.assertEqual(l_hex, 0x41)
        #
        l_hex = self.m_api._nibble_to_hex(0x0F)
        self.assertEqual(l_hex, 0x46)
        print('test_0101/  0x0f ==> {0:#2x} '.format(l_hex), l_hex)

    def test_0102_Byte2Hex(self):
        l_str = self.m_api._byte_to_2chars(0x00)
        self.assertEqual(l_str, b'\x30\x30')
        l_str = self.m_api._byte_to_2chars(0x08)
        self.assertEqual(l_str, '08')
        l_str = self.m_api._byte_to_2chars(0x0F)
        self.assertEqual(l_str, '0F')
        l_str = self.m_api._byte_to_2chars(0x80)
        self.assertEqual(l_str, '80')
        l_str = self.m_api._byte_to_2chars(0x77)
        self.assertEqual(l_str, '77')
        l_str = self.m_api._byte_to_2chars(0xff)
        self.assertEqual(l_str, 'FF')
        print('test_0102/  0xff ==> {0:} '.format(l_str), l_str)

    def test_0103_Checksum(self):
        l_ba = self.m_api._calculate_checksum(CHG_REG_CMD)
        self.assertEqual(l_ba, b'\x70\x03\x8D')
        print('test_0103-A/ Checksum {0:}'.format(PrintBytes(l_ba)))
        l_ba = self.m_api._calculate_checksum(b'\x35\x23\x24')
        self.assertEqual(l_ba, b'\x35\x23\x24\x84')
        print('test_0103-B/ Checksum {0:}'.format(PrintBytes(l_ba)))
        l_ba = self.m_api._calculate_checksum(b'\x11')
        self.assertEqual(l_ba, b'\x11\xEF')
        print('test_0103-C/ Checksum {0:}'.format(PrintBytes(l_ba)))
        l_ba = self.m_api._calculate_checksum(b'\xEF')
        self.assertEqual(l_ba, b'\xEF\x11')
        print('test_0103-D/ Checksum {0:}'.format(PrintBytes(l_ba)), l_ba)

    def test_0104_AssembleCommand(self):
        l_ba = self.m_api._assemble_regwrite(b'\x70', b'\x03')
        print('test_0104/ {0:}'.format(PrintBytes(l_ba)), l_ba)
        self.assertEqual(l_ba, b'\x70\x03\x8D')

    def test_0105_Convert(self):
        l_ba = self.m_api._assemble_regwrite(b'\x70', b'\x03')
        l_cv = self.m_api._convert_pim(l_ba)
        print('test_0105/ ', PrintBytes(l_cv), l_cv)
        self.assertEqual(l_cv, (b'\x37\x30\x30\x33\x38\x44'))

    def test_0106_Register(self):
        l_ba = self.m_api.write_register_command(self.m_controller_obj, b'\x70', b'\x03')
        print('test_0106/ ', PrintBytes(l_ba), l_ba)
        self.assertEqual(l_ba, (b'\x14\x37\x30\x30\x33\x38\x44\x0D'))


TEST_MESSAGE = b'\x15PE\r\x06'

class Test_02_Decode(unittest.TestCase):

    def setUp(self):
        self.m_api = UPB_Pim.DecodeResponses()
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Message = TEST_MESSAGE

    def test_0201_NextChar(self):
        pass

    def test_0210_ExtractMsg(self):
        print('Before', PrintBytes(self.m_controller_obj._Message))
        l_msg = self.m_api.decode_response(self.m_controller_obj)
        print(l_msg)
        print('After', PrintBytes(self.m_controller_obj._Message))

# ## END DBK
