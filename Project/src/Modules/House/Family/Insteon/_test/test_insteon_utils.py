"""
@name:      Modules/House/Family/insteon/_test/test_Insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 27, 2013
@summary:   This module is for testing Insteon conversion routines.

Passed all 23 tests - DBK - 2017-04-29

"""

__updated__ = '2019-09-26'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.House.Family.insteon import insteon_utils
from Modules.House.Family.insteon.insteon_utils import Util, Decode as utilDecode
from _test.testing_mixin import SetupPyHouseObj
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.debug_tools import FormatBytes

# this matches button 0 in XML_LIGHTING_BUTTONS
ADDR_BUTTON_0_MSG = bytearray(b'\x35\x6f\x2a')

ADDR_CONTROLLER_0_MSG = bytearray(b'\x21\x34\x1f')

ADDR_LIGHT_0_MSG = bytearray(b'\x16\x62\x2d')
ADDR_MOTION_0_MSG = bytearray(b'\x53\x22\x56')
ADDR_GARAGE_0_MSG = bytearray(b'\x16\x62\x2d')
ADDR_THERMOSTAT_0_MSG = bytearray(b'\x16\x62\x2d')

ADDR_DR_SLAVE_MSG = bytearray(b'\x16\xc9\xd0')

ADDR_NOOK_MSG = bytearray(b'\x17\xc2\x72')

INSTEON_0_MSG = bytearray(b'\x16\x62\x2d')
INSTEON_1_MSG = bytearray(b'\x21\x34\x1F')

MSG_50 = bytearray(b'\x02\x50\x53\x22\x56\x02\x04\x81\x27\x09\x00')

MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')

PORT_NAME = 'Updated Port Name'


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.inst = Util


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_Insteon_utils')


class A2_Command(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_60(self):
        l_cmd = insteon_utils.create_command_message('plm_info')
        # print('A2-01-A - ', FormatBytes(l_cmd))
        self.assertEqual(len(l_cmd), 2)
        self.assertEqual(l_cmd[0], 0x02)
        self.assertEqual(l_cmd[1], 0x60)

    def test_02_61(self):
        l_cmd = insteon_utils.create_command_message('all_link_send')
        # print('A2-02-A - ', FormatBytes(l_cmd))
        self.assertEqual(len(l_cmd), 5)
        self.assertEqual(l_cmd[0], 0x02)
        self.assertEqual(l_cmd[1], 0x61)

    def test_03_62(self):
        """
        """
        l_cmd = insteon_utils.create_command_message('insteon_send')
        # print('A2-03-A - ', FormatBytes(l_cmd))
        self.assertEqual(len(l_cmd), 8)
        self.assertEqual(l_cmd[0], 0x02)
        self.assertEqual(l_cmd[1], 0x62)


class A3_Queue(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Create(self):
        """
        """
        result = insteon_utils.create_command_message('insteon_send')
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A2-01-A - PyHouse'))
        self.assertEqual(len(result), 8)


class B1_Conversions(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_02_Addr(self):
        """
        """
        l_addr = '12.34.56'
        l_msg = bytearray(b'0000000000')
        l_ret = insteon_utils.insert_address_into_message(l_addr, l_msg, 2)
        print('B1-02-A - {}'.format(FormatBytes(l_ret)))

    def test_03_Addr(self):
        """
        """
        l_msg = bytearray(b'\x02\x62\x17\xc2\x02\x0f\x19\x00\x06')
        l_ret = insteon_utils.extract_address_from_message(l_msg, 2)
        print('B1-03-A Addr: {}'.format(l_ret))
        self.assertEqual(l_ret, '17.C2.02')


class D1_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Devcat(self):
        l_dev = b'\x02\x04'
        _l_ret = utilDecode._devcat(l_dev, self.m_obj)


class D2_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_GetObj(self):
        """
        """
        l_msg = MSG_50
        # print(FormatBytes(l_msg), 'D2-01-A - Message')
        _l_ret = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_msg[2:5])
        # print(PrettyFormatAny.form(_l_ret, 'D2-01-B - Combined Dicts'))


class E1_Lookup(SetupMixin, unittest.TestCase):
    """ Look up the object given its Insteon Address (which must be unique).
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_GetObj(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights[0], 'E1-01-A - Lighting'))
        l_addr = INSTEON_0_MSG
        _l_ret = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_addr)
        # print(PrettyFormatAny.form(l_ret, 'E1-01-B - Lighting'))


class F1_Update(SetupMixin, unittest.TestCase):
    """ Update the PyHouse store given an object with an insteon address.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PutLight(self):
        """
        """
        _l_light = self.m_pyhouse_obj.House.Lighting.Lights[0]
        # print(PrettyFormatAny.form(l_light, 'F1-01-A - Light'))
        l_addr = INSTEON_1_MSG
        l_ret = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_addr)
        l_ret.Port = PORT_NAME
        insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_ret)
        # print(PrettyFormatAny.form(l_light, 'F1-01-B - l_ret'))
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers[0].Port, PORT_NAME)

    def test_02_PutController(self):
        """
        """
        _l_controller = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        # print(PrettyFormatAny.form(l_controller, 'F1-02-A - Controller'))
        l_addr = INSTEON_1_MSG
        l_ret = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_addr)
        l_ret.Port = PORT_NAME
        insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_ret)
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

# ## END DBK
