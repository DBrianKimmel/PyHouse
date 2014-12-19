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
from Modules.Families import family
from Modules.Lighting.lighting_lights import LightingLightsAPI
from Modules.Lighting.lighting_controllers import LCApi
from test.xml_data import *
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny, PrintBytes


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
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = Insteon_PLM.API()
        self.m_llapi = LightingLightsAPI(self.m_pyhouse_obj)
        self.m_lcapi = LCApi(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.DeviceOBJs.Lights = self.m_llapi.read_all_lights_xml(self.m_xml.light_sect)
        self.m_pyhouse_obj.House.DeviceOBJs.Controllers = self.m_lcapi.read_all_controllers_xml(self.m_xml.controller_sect)
        self.m_controller = ControllerData()



class C01_Utility(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()


    def test_01_MessageLength(self):
        self.assertEqual(self.m_api._get_message_length(MSG_50), 11)
        self.assertEqual(self.m_api._get_message_length(MSG_62), 9)
        self.assertEqual(self.m_api._get_message_length(MSG_99), 1)

    def test_02_ExtractAddress(self):
        # self.assertEqual(self.m_api._get_addr_from_message(MSG_50, 2), conversions.dotted_hex2int(ADR_16C9D0))
        # self.assertEqual(self.m_api._get_addr_from_message(MSG_62, 2), conversions.dotted_hex2int(ADR_17C272))
        pass

    def test_03_Create(self):
        l_cmd = self.m_api._create_command_message('insteon_send')
        self.assertEqual(len(l_cmd), 8)
        self.assertEqual(l_cmd[0], STX)
        self.assertEqual(l_cmd[1], 0x62)

    def test_04_Obj(self):
        PrettyPrintAny(self.m_pyhouse_obj.House, 'House')
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'Devices')


class C02_Cmds(SetupMixin, unittest.TestCase):

    def setUp(self):
        # self.m_pyhouse_obj = PyHouseData()
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()

    def test_01_get_message_length(self):
        self.assertEqual(self.m_api._get_message_length(MSG_50), 11)
        self.assertEqual(self.m_api._get_message_length(MSG_62), 9)
        self.assertEqual(self.m_api._get_message_length(MSG_99), 1)

    def test_02_Command(self):
        l_cmd = self.m_api._create_command_message('insteon_send')
        print(PrintBytes(l_cmd))
        self.assertEqual(l_cmd[0], 0x02)
        self.assertEqual(l_cmd[1], 0x62)

    def test_03_63Cmd(self):
        l_obj = self.m_pyhouse_obj.House.DeviceOBJs.Lights[0]
        self.m_api._put_controller(self.m_controller)
        PrettyPrintAny(l_obj, 'Lights')
        l_cmd = self.m_api.queue_62_command(l_obj, 0x02, 0x04)


class C03_Driver(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_api = Insteon_PLM. API()

    def test_01_Driver(self):
        pass


class C04_Thermostat(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_controller_obj = ControllerData()

    def test_01_x(self):
        pass

# ## END DBK
