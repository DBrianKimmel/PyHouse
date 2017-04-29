"""
@name:      PyHouse/src/Modules/Families/Insteon/test/test_Insteon_decoder.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 18, 2014
@Summary:

Passed all 6 tests - DBK - 2016-10-31

This test needs the lighting controller data so it must be loaded,
also Light data and Thermostat data.
"""

__updated__ = '2017-04-26'

#  Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET


#  Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG
from Modules.Core.data_objects import ControllerData
from Modules.Families.Insteon import Insteon_decoder
from Modules.Families.Insteon.Insteon_utils import Util
from Modules.Families.family import API as familyAPI
from Modules.Housing.Hvac.hvac_xml import XML as hvacXML
from Modules.Housing.Lighting.lighting import Utility as lightingUtility
from Modules.Housing.Lighting.test.xml_controllers import TESTING_CONTROLLER_NAME_0
from Modules.Housing.Security.security import XML as securityXML
from Modules.Core.Utilities.debug_tools import FormatBytes
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_50T = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x6e\x4f')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')
MSG_99 = bytearray(b'\x02\x99')


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj.House.FamilyData = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.Lighting = lightingUtility()._read_lighting_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Security.GarageDoors = securityXML().read_all_GarageDoors_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Security.MotionSensors = securityXML().read_all_MotionSensors_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Hvac = hvacXML.read_hvac_xml(self.m_pyhouse_obj)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_Insteon_decoder')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that the Setup and the XML is correct for this test module.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """Test that PyHouse_obj has the needed info.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-01-B - PyHouse.House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting, 'A1-01-C - PyHouse.House.Lighting', 80))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Security, 'A1-01-D - PyHouse.House.Security', 80))
        self.assertEqual(self.m_pyhouse_obj.Xml.XmlFileName, '/etc/pyhouse/master.xml')
        self.assertEqual(len(self.m_pyhouse_obj.House.Lighting.Buttons), 2)
        self.assertEqual(len(self.m_pyhouse_obj.House.Lighting.Controllers), 2)
        self.assertEqual(len(self.m_pyhouse_obj.House.Security.GarageDoors), 1)
        self.assertEqual(len(self.m_pyhouse_obj.House.Lighting.Lights), 2)
        self.assertEqual(len(self.m_pyhouse_obj.House.Security.MotionSensors), 1)

    def test_02_House(self):
        #  print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse.House'))
        pass

    def test_03_Controller(self):
        l_ctlr = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        # print(PrettyFormatAny.form(l_ctlr, 'A1-03-A - PyHouse.House.Lighting.Controllers[0]'))
        self.assertEqual(l_ctlr.Name, TESTING_CONTROLLER_NAME_0)


class B1_Util(SetupMixin, unittest.TestCase):
    """This tests the utility section of decoding
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_ctrlr = ControllerData()

    def test_01_GetObjFromMsg(self):
        self.m_ctrlr._Message = MSG_50
        l_ctlr = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        # print(PrettyFormatAny.form(l_ctlr, 'B1-01-A Controller'))
        self.assertEqual(l_ctlr.Name, TESTING_CONTROLLER_NAME_0)

    def test_02_NextMsg(self):
        self.m_ctrlr._Message = MSG_50
        l_msg = Util().get_next_message(self.m_ctrlr)
        print(FormatBytes(l_msg))
        #  self.assertEqual(l_msg[1], 0x50)
        #  self.m_ctrlr._Message = bytearray()
        #  l_msg = self.m_util.get_next_message(self.m_ctrlr)
        #  self.assertEqual(l_msg, None)
        #  self.m_ctrlr._Message = MSG_62 + MSG_50
        #  l_msg = self.m_util.get_next_message(self.m_ctrlr)
        #  print('Msg {}'.format(FormatBytes(l_msg)))
        #  print('remaning: {}'.format(FormatBytes(self.m_ctrlr._Message)))
        #  self.assertEqual(l_msg[1], 0x62)
        self.assertEqual(self.m_ctrlr._Message[1], 0x50)


class B2_Decode(SetupMixin, unittest.TestCase):
    """This tests the utility section of decoding
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_ctrlr = ControllerData()
        self.m_decode = Insteon_decoder.DecodeResponses(self.m_pyhouse_obj, self.m_ctrlr)

    def test_01_GetObjFromMsg(self):
        self.m_ctrlr._Message = MSG_50
        l_ctlr = self.m_decode.decode_message(self.m_ctrlr)
        print(l_ctlr, 'B2-01-A Controller')


class T1_HVAC(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_ctrlr = self.m_pyhouse_obj.House
        #  print(PrettyFormatAny.form(self.m_ctrlr, "Controlelrs"))
        self.m_ctrlr = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        #  print(PrettyFormatAny.form(self.m_ctrlr, "Controlelrs"))
        self.m_decode = Insteon_decoder.DecodeResponses(self.m_pyhouse_obj, self.m_ctrlr)

    def test_01_x(self):
        self.m_ctrlr._Message = MSG_50T
        self.m_pyhouse_obj.House.Lighting.Controllers[0]
        self.m_decode.decode_message(self.m_ctrlr)
        # print(PrettyFormatAny.form(self.m_ctrlr, "T1-01-A - Controller"))
        self.assertEqual(len(self.m_ctrlr._Message), 0)

#  ## END DBK
