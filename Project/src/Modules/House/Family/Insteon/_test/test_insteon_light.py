"""
@name:      PyHouse/src/Modules/Families/Insteon/_test/test_Insteon_HVAC.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 6, 2014
@Summary:

Passed all 2 tests - DBK - 2015-07-29

"""

__updated__ = '2020-02-17'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Lighting.Controllers.controllers import Api as controllerApi
from Modules.House.Lighting.Lights.lights import Api as lightingApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Family.Insteon.insteon_utils import Decode as utilDecode
from Modules.House.Family.Insteon import insteon_decoder
from Modules.House.Family.Insteon.insteon_light import DecodeResponses as Decode_Light

# 16.C9.D0 =
# 1B.47.81 =
MSG_50_A = bytearray(b'\x02\x50\x16\x62\x2d\x1b\x47\x81\x27\x09\x00')
MSG_50_B = bytearray(b'\x02\x50\x21\x34\x1F\x1b\x47\x81\x27\x6e\x4f')


class DummyApi:

    def MqttPublish(self, p_topic, p_msg):
        return


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_xml = SetupPyHouseObj().BuildXml()
        self.m_cntl_api = controllerApi()
        self.m_light_api = lightingApi()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_Insteon_Light')


class A1_Prep(SetupMixin, unittest.TestCase):
    """ This section tests the setup
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_device = None

    def test_01_PyHouse(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)

    def test_02_FindXml(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')

    def test_03_House(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_04_Objs(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_05_XML(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_06_Device(self):
        """ Be sure that the XML contains the right stuff.
        """


class B1_Util(SetupMixin, unittest.TestCase):
    """This tests the utility section of decoding
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_ctrlr = ControllerInformation()

    def test_01_GetObjFromMsg(self):
        self.m_ctrlr._Message = MSG_50_A
        self.m_controllers = self.m_cntl_api.read_all_controllers_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Lighting.Controllers = self.m_controllers
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting, 'B1-01-A Lighting'))
        l_ctlr = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        print(PrettyFormatAny.form(l_ctlr, 'B1-01-B Controller'))
        self.assertEqual(l_ctlr.Name, TESTING_CONTROLLER_NAME_0)

    def test_02_NextMsg(self):
        self.m_ctrlr._Message = MSG_50_A
        # l_msg = Util().get_next_message(self.m_ctrlr)
        # print(PrintBytes(l_msg))
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
        SetupMixin.setUp(self)
        self.m_ctrlr = ControllerInformation()
        self.m_decode = Insteon_decoder.DecodeResponses(self.m_pyhouse_obj, self.m_ctrlr)

    def test_01_GetObjFromMsg(self):
        self.m_ctrlr._Message = MSG_50_A
        l_ctlr = self.m_decode.decode_message(self.m_ctrlr)
        print(l_ctlr, 'B2-01-A Controller')


class C1_Light(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_pyhouse_obj.House.Lighting.Controllers = self.m_cntl_api.read_all_controllers_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Lighting.Lights = self.m_light_api.read_all_lights_xml(self.m_pyhouse_obj)
        self.m_ctrlr = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        # print(PrettyFormatAny.form(self.m_ctrlr, "C1-0Controlelrs"))
        self.m_pyhouse_obj.Core.MqttApi = DummyApi()

    def test_01_x(self):
        self.m_ctrlr._Message = MSG_50_A
        l_device_obj = utilDecode().get_obj_from_message(self.m_pyhouse_obj, self.m_ctrlr._Message[2:5])

        l_decode = Decode_Light().decode_0x50(self.m_pyhouse_obj, self.m_ctrlr, l_device_obj)
        print(PrettyFormatAny.form(l_device_obj, "C1-01-A - Decode"))
        self.assertEqual(len(self.m_ctrlr._Message), 0)

    def test_02_x(self):
        self.m_ctrlr._Message = MSG_50_B
        l_device_obj = utilDecode().get_obj_from_message(self.m_pyhouse_obj, self.m_ctrlr._Message[2:5])

        l_decode = Decode_Light().decode_0x50(self.m_pyhouse_obj, self.m_ctrlr, l_device_obj)
        print(PrettyFormatAny.form(l_device_obj, "C1-02-A - Decode"))
        self.assertEqual(len(self.m_ctrlr._Message), 0)

#  ## END DBK
