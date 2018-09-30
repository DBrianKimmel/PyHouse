"""
@name:      PyHouse/src/Modules/Famlies/UPB/test/test_UPB_Pim.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test the UPB controller.

Passed all 30 tests - DBK - 2015-08-15

"""

__updated__ = '2017-04-26'


# Import system type stuff
try:
    import Queue
except ImportError:
    import queue as Queue
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families.UPB.UPB_Pim import BuildCommand, DecodeResponses
from Modules.Core.data_objects import ControllerData
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG

CHG_REG_CMD = b'\x70\x03'
WE_SEND_CHREG = b'\x17\x70\x03\x8D\x0D'

TEST_MESSAGE = b'\x15PE\r\x06'


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        pass


class B1_Build(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Queue = Queue.Queue(300)

    def test_01_Nibble2Hex(self):
        """Convert nibbles to the hex char representation
        """
        l_hex = BuildCommand._nibble_to_hex(0x00)
        self.assertEqual(l_hex, ord('0'))
        #
        l_hex = BuildCommand._nibble_to_hex(0x07)
        self.assertEqual(l_hex, ord('7'))
        #
        l_hex = BuildCommand._nibble_to_hex(0x0A)
        self.assertEqual(l_hex, 0x41)
        #
        l_hex = BuildCommand._nibble_to_hex(0x0F)
        self.assertEqual(l_hex, 0x46)

    def test_02_Byte2Hex(self):
        l_str = BuildCommand._byte_to_2chars(0x00)
        self.assertEqual(l_str, b'\x30\x30')
        self.assertEqual(l_str, '00')
        l_str = BuildCommand._byte_to_2chars(0x08)
        self.assertEqual(l_str, '08')
        l_str = BuildCommand._byte_to_2chars(0x0F)
        self.assertEqual(l_str, '0F')
        l_str = BuildCommand._byte_to_2chars(0x80)
        self.assertEqual(l_str, '80')
        l_str = BuildCommand._byte_to_2chars(0x77)
        self.assertEqual(l_str, '77')
        l_str = BuildCommand._byte_to_2chars(0xff)
        self.assertEqual(l_str, 'FF')

    def test_03_CalcChecksum(self):
        l_ba = BuildCommand._calculate_checksum(b'\x11')
        self.assertEqual(l_ba, ord(b'\xEF'))
        #
        l_ba = BuildCommand._calculate_checksum(b'\xD4')
        self.assertEqual(l_ba, ord(b'\x2C'))
        #
        l_ba = BuildCommand._calculate_checksum(b'\x70\x03')
        self.assertEqual(l_ba, ord(b'\x8D'))
        #
        l_ba = BuildCommand._calculate_checksum(b'\xA1\xA3')
        self.assertEqual(l_ba, ord(b'\xBC'))
        #
        l_ba = BuildCommand._calculate_checksum(b'\x51\xA3\x6A')
        # print('5 {} {:x}'.format(l_ba, l_ba))
        self.assertEqual(l_ba, ord(b'\xA2'))
        #
        l_ba = BuildCommand._calculate_checksum(b'\x35\x23\x24\x9f')
        # print('6 {} {:x}'.format(l_ba, l_ba))
        self.assertEqual(l_ba, ord(b'\xE5'))

    def test_04_AppendChecksum(self):
        l_ba = BuildCommand._append_checksum(b'\x70\x03')
        self.assertEqual(l_ba, b'\x70\x03\x8D')

    def test_05_AssembleCommand(self):
        l_ba = BuildCommand._assemble_regwrite(0x70, b'\03')
        self.assertEqual(l_ba, b'\x70\x03\x8D')

    def test_06_Convert(self):
        l_ba = BuildCommand._assemble_regwrite(0x70, b'\x03')
        l_cv = BuildCommand._convert_pim(l_ba)
        self.assertEqual(l_cv, (b'\x70\x03\x8D'))

    def test_07_CreateHeader(self):
        pass

    def test_08_QueueCommand(self):
        pass

    def test_09_Register(self):
        l_ba = BuildCommand.write_register_command(self.m_controller_obj, b'\x70', b'\x03')
        self.assertEqual(l_ba, (b'\x17\x70\x03\x8D\x0D'))

    def test_10_WritePim(self):
        pass


class B2_Util(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_api = DecodeResponses()
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Message = TEST_MESSAGE

    def test_01_NextChar(self):
        pass


class B3_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_api = DecodeResponses()
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Message = TEST_MESSAGE

    def test_01_GetRest(self):
        pass

    def test_02_ExtractMsg(self):
        # print('Before', FormatBytes(self.m_controller_obj._Message))
        l_msg = self.m_api.decode_response(self.m_controller_obj)
        # print(l_msg)
        # print('After', FormatBytes(self.m_controller_obj._Message))

    def test_03_DispatchDecode(self):
        pass

    def test_04_DecodeResponse(self):
        pass

    def test_05_DecodeA(self):
        pass

    def test_06_DecodeB(self):
        pass

    def test_07_DecodeE(self):
        pass

    def test_08_DecodeK(self):
        pass

    def test_09_DecodeN(self):
        pass

    def test_10DecodeR(self):
        pass

    def test_11_DecodeU(self):
        pass


class B4_Driver(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_api = DecodeResponses()
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Message = TEST_MESSAGE

    def test_01_LoopStart(self):
        pass

    def test_02_QueueCommand(self):
        pass

    def test_03_DequeSend(self):
        pass

    def test_04_ReceiveLoop(self):
        pass


class B5_Create(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        pass


class B6_PimAPI(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        pass

class C1_API(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        pass

# ## END DBK
