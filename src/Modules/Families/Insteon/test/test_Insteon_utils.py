"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 27, 2013
@summary:   This module is for testing Insteon conversion routines.

Passed all 14 tests - DBK - 2016-09-30

"""

__updated__ = '2016-10-06'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Core import conversions
from Modules.Families.Insteon import Insteon_utils
from Modules.Families.Insteon.Insteon_utils import Util, Decode as utilDecode
from Modules.Housing.Lighting.lighting import Utility
from test.testing_mixin import SetupPyHouseObj
from Modules.Families.Insteon.test.xml_insteon import TESTING_INSTEON_ADDRESS_0, \
    TESTING_INSTEON_ADDRESS_1
from test.xml_data import XML_LONG
from Modules.Utilities.debug_tools import PrettyFormatAny
# from Modules.Utilities.tools import PrintBytes

ADDR_DR_SLAVE_MSG = bytearray(b'\x16\xc9\xd0')
ADDR_DR_SLAVE_INT = (((0x16 * 256) + 0xc9) * 256) + 0xd0  # 1493456

ADDR_NOOK_MSG = bytearray(b'\x17\xc2\x72')
ADDR_NOOK_INT = (((0x17 * 256) + 0xc2) * 256) + 0x72  #  1557106

INSTEON_0_MSG = bytearray(b'\x16\x62\x2d')
INSTEON_1_MSG = bytearray(b'\x21\x34\x1F')

MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x02\x04\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')

PORT_NAME = 'Updated Port Name'


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_obj = ControllerData()
        self.inst = Util


class A1_Command(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Create(self):
        """ Get 3 bytes and convert it ti a laww
        """
        result = Insteon_utils.create_command_message('insteon_send')
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse'))
        self.assertEqual(len(result), 8)



class A2_Queue(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Create(self):
        """ Get 3 bytes and convert it ti a laww
        """
        result = Insteon_utils.create_command_message('insteon_send')
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse'))
        self.assertEqual(len(result), 8)


class B1_Conversions(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Message2int(self):
        """ Get 3 bytes and convert it ti a laww
        """
        result = self.inst.message2int(MSG_50[2:5])
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse'))
        self.assertEqual(result, ADDR_DR_SLAVE_INT)
        #
        result = self.inst.message2int(MSG_62[2:5])
        self.assertEqual(result, ADDR_NOOK_INT)


class C1_Conversions(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Message2int(self):
        """ Get 3 bytes and convert it ti a laww
        """
        result = self.inst.message2int(MSG_50[2:5])
        # print(result)
        self.assertEqual(result, ADDR_DR_SLAVE_INT)
        #
        result = self.inst.message2int(MSG_62[2:5])
        self.assertEqual(result, ADDR_NOOK_INT)

    def test_02_Int2message(self):
        """ Convert a long int to a 3 byte address
        """
        l_msg = MSG_50
        result = self.inst.int2message(ADDR_DR_SLAVE_INT, l_msg, 2)
        # print(PrintBytes(result))
        self.assertEqual(result[2:5], ADDR_DR_SLAVE_MSG)
        #
        l_msg = MSG_62
        result = self.inst.int2message(ADDR_NOOK_INT, l_msg, 2)
        self.assertEqual(result[2:5], ADDR_NOOK_MSG)

    def test_03_Json(self):
        pass


class D1_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Devcat(self):
        l_dev = b'\x02\x04'
        _l_ret = utilDecode._devcat(l_dev, self.m_obj)
        # print(PrettyFormatAny.form(l_ret, 'D1-01-A - xxx'))
        self.assertEqual(self.m_obj.DevCat, 0x0204)
        #
        l_dev = MSG_50
        # l_c = l_dev[5:7]
        # print(FormatBytes(l_c))
        _l_ret = utilDecode._devcat(l_dev[5:7], self.m_obj)
        self.assertEqual(self.m_obj.DevCat, 0x0204)


class D2_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_02_GetObj(self):
        """
        """
        l_msg = MSG_50
        # print(PrintBytes(l_msg), 'D2-01-A - Message')
        _l_ret = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_msg)
        # print(l_ret)
        # print(PrettyFormatAny.form(l_ret, 'Combined Dicts'))


class E1_Lookup(SetupMixin, unittest.TestCase):
    """ Look up the object given its Insteon Address (which must be unique).
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        Utility()._read_lighting_xml(self.m_pyhouse_obj)

    def test_01_GetObj(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights[0], 'E1-01-A - Lighting'))
        l_addr = INSTEON_0_MSG
        l_ret = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_addr)
        l_dotted = conversions.int2dotted_hex(l_ret.InsteonAddress, 3)
        # print(PrettyFormatAny.form(l_ret, 'E1-01-B - Lighting'))
        self.assertEqual(l_dotted, TESTING_INSTEON_ADDRESS_0)


class F1_Update(SetupMixin, unittest.TestCase):
    """ Update the PyHouse store given an object with an insteon address.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        Utility()._read_lighting_xml(self.m_pyhouse_obj)

    def test_01_PutLight(self):
        """
        """
        l_light = self.m_pyhouse_obj.House.Lighting.Lights[0]
        print(PrettyFormatAny.form(l_light, 'F1-01-A - Light'))
        l_addr = INSTEON_1_MSG
        l_ret = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_addr)
        l_ret.Port = PORT_NAME
        Insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_ret)
        print(PrettyFormatAny.form(l_light, 'F1-01-B - l_ret'))
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers[0].Port, PORT_NAME)

    def test_02_PutController(self):
        """
        """
        l_controller = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        print(PrettyFormatAny.form(l_controller, 'F1-02-A - Controller'))
        l_addr = INSTEON_1_MSG
        l_ret = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_addr)
        l_ret.Port = PORT_NAME
        Insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_ret)
        print(PrettyFormatAny.form(l_controller, 'F1-02-B - l_ret'))
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers[0].Port, PORT_NAME)

    def test_03_PutButton(self):
        """
        """
        l_controller = self.m_pyhouse_obj.House.Lighting.Buttons[0]
        print(PrettyFormatAny.form(l_controller, 'F1-03-A - Button'))

    def test_04_PutThermostat(self):
        """
        """
        l_thermostat = self.m_pyhouse_obj.House.Hvac.Thermostats[0]
        print(PrettyFormatAny.form(l_thermostat, 'F1-04-A - Thermostat'))

    def test_05_PutGarageDoor(self):
        """
        """
        l_garage = self.m_pyhouse_obj.House.Lighting.Buttons[0]
        print(PrettyFormatAny.form(l_garage, 'F1-05-A - Garage'))

class J1_Json(SetupMixin, unittest.TestCase):
    """ Update the PyHouse store given an object with an insteon address.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        Utility()._read_lighting_xml(self.m_pyhouse_obj)

    def test_01_get(self):
        """
        """

 # ## END DBK
