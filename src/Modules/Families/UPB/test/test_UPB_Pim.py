"""
@name:      PyHouse/src/Modules/Famlies/UPB/test/test_UPB_Pim.py
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
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Families.UPB import UPB_Pim
from Modules.Core.data_objects import ControllerData
from Modules.Utilities.tools import PrintBytes  # , PrettyPrintAny
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG

CHG_REG_CMD = b'\x70\x03'
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
        self.m_api = UPB_Pim.BuildCommand()
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Queue = Queue.Queue(300)

    def test_01_Nibble2Hex(self):
        l_hex = self.m_api._nibble_to_hex(0x00)
        self.assertEqual(l_hex, ord('0'))
        #
        l_hex = self.m_api._nibble_to_hex(0x07)
        self.assertEqual(l_hex, ord('7'))
        #
        l_hex = self.m_api._nibble_to_hex(0x0A)
        self.assertEqual(l_hex, 0x41)
        #
        l_hex = self.m_api._nibble_to_hex(0x0F)
        self.assertEqual(l_hex, 0x46)

    def test_02_Byte2Hex(self):
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

    def test_03_Checksum(self):
        l_ba = self.m_api._calculate_checksum(CHG_REG_CMD)
        self.assertEqual(l_ba, b'\x70\x03\x8D')
        # print('test_0103-A/ Checksum {0:}'.format(PrintBytes(l_ba)))
        l_ba = self.m_api._calculate_checksum(b'\x35\x23\x24')
        self.assertEqual(l_ba, b'\x35\x23\x24\x84')
        # print('test_0103-B/ Checksum {0:}'.format(PrintBytes(l_ba)))
        l_ba = self.m_api._calculate_checksum(b'\x11')
        self.assertEqual(l_ba, b'\x11\xEF')
        # print('test_0103-C/ Checksum {0:}'.format(PrintBytes(l_ba)))
        l_ba = self.m_api._calculate_checksum(b'\xEF')
        self.assertEqual(l_ba, b'\xEF\x11')
        # print('test_0103-D/ Checksum {0:}'.format(PrintBytes(l_ba)), l_ba)

    def test_04_AssembleCommand(self):
        l_ba = self.m_api._assemble_regwrite(b'\x70', b'\x03')
        # print('test_0104/ {0:}'.format(PrintBytes(l_ba)), l_ba)
        self.assertEqual(l_ba, b'\x70\x03\x8D')

    def test_05_Convert(self):
        l_ba = self.m_api._assemble_regwrite(b'\x70', b'\x03')
        l_cv = self.m_api._convert_pim(l_ba)
        # print('test_0105/ ', PrintBytes(l_cv), l_cv)
        self.assertEqual(l_cv, (b'\x37\x30\x30\x33\x38\x44'))

    def test_06_CreateHeader(self):
        pass

    def test_07_QueueCommand(self):
        pass

    def test_08_Register(self):
        l_ba = self.m_api.write_register_command(self.m_controller_obj, b'\x70', b'\x03')
        # print('test_0106/ ', PrintBytes(l_ba), l_ba)
        self.assertEqual(l_ba, (b'\x14\x37\x30\x30\x33\x38\x44\x0D'))

    def test_09_WritePim(self):
        pass


class B2_Util(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_api = UPB_Pim.DecodeResponses()
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Message = TEST_MESSAGE

    def test_01_NextChar(self):
        pass


class B3_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_api = UPB_Pim.DecodeResponses()
        self.m_controller_obj = ControllerData()
        self.m_controller_obj._Message = TEST_MESSAGE

    def test_01_GetRest(self):
        pass

    def test_02_ExtractMsg(self):
        # print('Before', PrintBytes(self.m_controller_obj._Message))
        l_msg = self.m_api.decode_response(self.m_controller_obj)
        # print(l_msg)
        # print('After', PrintBytes(self.m_controller_obj._Message))

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
        self.m_api = UPB_Pim.DecodeResponses()
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
