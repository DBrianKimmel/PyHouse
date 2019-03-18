"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 27, 2013
@summary:   This module is for testing Insteon conversion routines.

Passed all 23 tests - DBK - 2017-04-29

"""

__updated__ = '2019-03-18'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Core import conversions
from Modules.Families.family import API as familyAPI
from Modules.Families.Insteon import Insteon_utils
from Modules.Families.Insteon.Insteon_utils import Util, Decode as utilDecode
from Modules.Housing.Hvac.hvac_xml import XML as hvacXML
from Modules.Housing.Lighting.lighting import Utility as lightingUtility
from Modules.Housing.Lighting.test.xml_buttons import \
    TESTING_LIGHTING_BUTTON_DEVICE_TYPE_0, \
    TESTING_LIGHTING_BUTTON_DEVICE_SUBTYPE_0
from test.testing_mixin import SetupPyHouseObj
from Modules.Families.Insteon.test.xml_insteon import \
    TESTING_INSTEON_ADDRESS_0
from test.xml_data import XML_LONG
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.debug_tools import FormatBytes

# this matches button 0 in XML_LIGHTING_BUTTONS
ADDR_BUTTON_0_MSG = bytearray(b'\x35\x6f\x2a')
ADDR_BUTTON_0_INT = (((0x35 * 256) + 0x6f) * 256) + 0x2a

ADDR_CONTROLLER_0_MSG = bytearray(b'\x21\x34\x1f')
ADDR_CONTROLLER_0_INT = (((0x21 * 256) + 0x34) * 256) + 0x1f

ADDR_LIGHT_0_MSG = bytearray(b'\x16\x62\x2d')
ADDR_MOTION_0_MSG = bytearray(b'\x53\x22\x56')
ADDR_GARAGE_0_MSG = bytearray(b'\x16\x62\x2d')
ADDR_THERMOSTAT_0_MSG = bytearray(b'\x16\x62\x2d')

ADDR_DR_SLAVE_MSG = bytearray(b'\x16\xc9\xd0')
ADDR_DR_SLAVE_INT = (((0x16 * 256) + 0xc9) * 256) + 0xd0

ADDR_NOOK_MSG = bytearray(b'\x17\xc2\x72')
ADDR_NOOK_INT = (((0x17 * 256) + 0xc2) * 256) + 0x72  #  1557106

INSTEON_0_MSG = bytearray(b'\x16\x62\x2d')
INSTEON_0_INT = (((0x16 * 256) + 0x62) * 256) + 0x2d  #  1557106
INSTEON_1_MSG = bytearray(b'\x21\x34\x1F')

MSG_50 = bytearray(b'\x02\x50\x53\x22\x56\x02\x04\x81\x27\x09\x00')
MSG_50_INT = (((0x53 * 256) + 0x22) * 256) + 0x56  #  1557106

MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')
MSG_62_INT = (((0x17 * 256) + 0xc2) * 256) + 0x72  #  1557106

PORT_NAME = 'Updated Port Name'


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_obj = ControllerData()
        self.inst = Util
        self.m_pyhouse_obj.FamilyInformation = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.Lighting = lightingUtility()._read_lighting_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Hvac = hvacXML.read_hvac_xml(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Insteon_utils')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Create(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml.XmlRoot, 'A1-01-A - XML'))
        pass


class A2_Command(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_60(self):
        l_cmd = Insteon_utils.create_command_message('plm_info')
        # print('A2-01-A - ', FormatBytes(l_cmd))
        self.assertEqual(len(l_cmd), 2)
        self.assertEqual(l_cmd[0], 0x02)
        self.assertEqual(l_cmd[1], 0x60)

    def test_02_61(self):
        l_cmd = Insteon_utils.create_command_message('all_link_send')
        # print('A2-02-A - ', FormatBytes(l_cmd))
        self.assertEqual(len(l_cmd), 5)
        self.assertEqual(l_cmd[0], 0x02)
        self.assertEqual(l_cmd[1], 0x61)

    def test_03_62(self):
        """
        """
        l_cmd = Insteon_utils.create_command_message('insteon_send')
        # print('A2-03-A - ', FormatBytes(l_cmd))
        self.assertEqual(len(l_cmd), 8)
        self.assertEqual(l_cmd[0], 0x02)
        self.assertEqual(l_cmd[1], 0x62)


class A3_Queue(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Create(self):
        """
        """
        result = Insteon_utils.create_command_message('insteon_send')
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A2-01-A - PyHouse'))
        self.assertEqual(len(result), 8)


class B1_Conversions(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Message2int(self):
        """ Get 3 bytes and convert it t0 a long
        """
        result = self.inst.message2int(MSG_50[2:5])
        # print(PrettyFormatAny.form(result, 'B1-01-A - PyHouse'))
        # print((result))
        self.assertEqual(result, MSG_50_INT)
        #
        result = self.inst.message2int(MSG_62[2:5])
        self.assertEqual(result, MSG_62_INT)


class B2_Lookup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Button(self):
        """
        """
        result = utilDecode._find_addr_one_class(self.m_pyhouse_obj, self.m_pyhouse_obj.House.Lighting.Buttons, ADDR_BUTTON_0_INT)
        # print(PrettyFormatAny.form(result, 'B2-01-A - PyHouse'))
        # print((result))
        self.assertEqual(result.InsteonAddress, ADDR_BUTTON_0_INT)


class B3_Lookup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Button(self):
        """
        """
        result = utilDecode.find_address_all_classes(self.m_pyhouse_obj, ADDR_BUTTON_0_INT)
        # print(PrettyFormatAny.form(result, 'B3-01-A - PyHouse'))
        # print((result))
        self.assertEqual(result.InsteonAddress, ADDR_BUTTON_0_INT)
        self.assertEqual(str(result.DeviceType), TESTING_LIGHTING_BUTTON_DEVICE_TYPE_0)
        self.assertEqual(str(result.DeviceSubType), TESTING_LIGHTING_BUTTON_DEVICE_SUBTYPE_0)

    def test_01_Controller(self):
        """
        """
        result = utilDecode.find_address_all_classes(self.m_pyhouse_obj, ADDR_CONTROLLER_0_INT)
        # print(PrettyFormatAny.form(result, 'B3-01-A - PyHouse'))
        # print((result))
        self.assertEqual(result.InsteonAddress, ADDR_CONTROLLER_0_INT)


class C1_Convert(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Message2int(self):
        """ Get 3 bytes and convert it to a long int
        """
        result = self.inst.message2int(MSG_50[2:5])
        # print('C1-01-A - ', FormatBytes(MSG_50[2:5]), result)
        self.assertEqual(result, MSG_50_INT)
        #
        result = self.inst.message2int(MSG_62[2:5])
        self.assertEqual(result, MSG_62_INT)

    def test_02_i2msg(self):
        """ Convert a long int to a 3 byte address
        """
        l_msg = bytearray(b'0000000000')
        result = self.inst.int2message(ADDR_DR_SLAVE_INT, l_msg, 2)
        # print('C1-02-A - ', FormatBytes(result))
        # print('C1-02-B - ', FormatBytes(l_msg))
        self.assertEqual(result[2:5], ADDR_DR_SLAVE_MSG)
        #

    def test_03_i2msg(self):
        """ Convert a long int to a 3 byte address
        """
        l_msg = bytearray(b'          ')
        result = self.inst.int2message(ADDR_NOOK_INT, l_msg, 2)
        # print('C1-03-A - ', FormatBytes(result))
        # print('C1-03-B - ', FormatBytes(l_msg))
        self.assertEqual(result[2:5], ADDR_NOOK_MSG)

    def test_04_Json(self):
        pass


class D1_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Devcat(self):
        l_dev = b'\x02\x04'
        _l_ret = utilDecode._devcat(l_dev, self.m_obj)
        # print(PrettyFormatAny.form(_l_ret, 'D1-01-A - xxx'))
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

    def test_01_GetObj(self):
        """
        """
        l_msg = MSG_50
        # print(FormatBytes(l_msg), 'D2-01-A - Message')
        _l_ret = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_msg[2:5])
        # print(PrettyFormatAny.form(_l_ret, 'D2-01-B - Combined Dicts'))


class E1_Lookup(SetupMixin, unittest.TestCase):
    """ Look up the object given its Insteon Address (which must be unique).
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        lightingUtility()._read_lighting_xml(self.m_pyhouse_obj)

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
        lightingUtility()._read_lighting_xml(self.m_pyhouse_obj)

    def test_01_PutLight(self):
        """
        """
        _l_light = self.m_pyhouse_obj.House.Lighting.Lights[0]
        # print(PrettyFormatAny.form(l_light, 'F1-01-A - Light'))
        l_addr = INSTEON_1_MSG
        l_ret = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_addr)
        l_ret.Port = PORT_NAME
        Insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_ret)
        # print(PrettyFormatAny.form(l_light, 'F1-01-B - l_ret'))
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers[0].Port, PORT_NAME)

    def test_02_PutController(self):
        """
        """
        _l_controller = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        # print(PrettyFormatAny.form(l_controller, 'F1-02-A - Controller'))
        l_addr = INSTEON_1_MSG
        l_ret = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_addr)
        l_ret.Port = PORT_NAME
        Insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_ret)
        # print(PrettyFormatAny.form(l_controller, 'F1-02-B - l_ret'))
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers[0].Port, PORT_NAME)

    def test_03_PutButton(self):
        """
        """
        _l_controller = self.m_pyhouse_obj.House.Lighting.Buttons[0]
        # print(PrettyFormatAny.form(l_controller, 'F1-03-A - Button'))

    def test_04_PutThermostat(self):
        """
        """
        _l_thermostat = self.m_pyhouse_obj.House.Hvac.Thermostats[0]
        # print(PrettyFormatAny.form(l_thermostat, 'F1-04-A - Thermostat'))

    def test_05_PutGarageDoor(self):
        """
        """
        _l_garage = self.m_pyhouse_obj.House.Lighting.Buttons[0]
        # print(PrettyFormatAny.form(l_garage, 'F1-05-A - Garage'))


class J1_Json(SetupMixin, unittest.TestCase):
    """ Update the PyHouse store given an object with an insteon address.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        lightingUtility()._read_lighting_xml(self.m_pyhouse_obj)

    def test_01_get(self):
        """
        """

# ## END DBK
