"""
@name:      PyHouse/src/Modules/Families/Insteon/test/test_Insteon_decoder.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c)  2014 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 18, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import ControllerData
from Modules.Families.Insteon import Insteon_decoder
from Modules.Families import family
from Modules.Lighting.lighting_lights import API as lightsAPI
from Modules.Lighting.lighting_controllers import API as controllerAPI
from test.xml_data import *
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny, PrintBytes
# from Modules.Computer.Internet.internet_xml import Util



MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')
MSG_99 = bytearray(b'\x02\x99')



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)



class C00_Setup(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_pyhouse_obj.House.DeviceOBJs.Controllers = controllerAPI(self.m_pyhouse_obj).read_all_controllers_xml(self.m_xml.controller_sect)
        self.m_pyhouse_obj.House.DeviceOBJs.Lights = lightsAPI.read_all_lights_xml(self.m_pyhouse_obj, self.m_xml.controller_sect)

    def test_01_PyHouse(self):
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        l_house = self.m_pyhouse_obj.House
        PrettyPrintAny(l_house, 'House')
        l_devs = l_house.DeviceOBJs
        PrettyPrintAny(l_devs, 'Devices')
        l_refs = l_house.RefOBJs
        PrettyPrintAny(l_refs, 'References')


class C01_Util(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_ctrlr = ControllerData()
        self.m_util = Insteon_decoder.D_Util


    def test_01_Drop1st(self):
        self.m_ctrlr._Message = bytearray(b'\x04')
        self.m_util._drop_first_byte(self.m_ctrlr)
        self.assertEqual(len(self.m_ctrlr._Message), 0)

    def test_02_NextMsg(self):
        self.m_ctrlr._Message = MSG_50
        l_msg = self.m_util.get_next_message(self.m_ctrlr)
        print(PrintBytes(l_msg))
        self.assertEqual(l_msg[1], 0x50)
        self.m_ctrlr._Message = bytearray()
        l_msg = self.m_util.get_next_message(self.m_ctrlr)
        self.assertEqual(l_msg, None)
        self.m_ctrlr._Message = MSG_62 + MSG_50
        l_msg = self.m_util.get_next_message(self.m_ctrlr)
        print('Msg {}'.format(PrintBytes(l_msg)))
        print('remaning: {}'.format(PrintBytes(self.m_ctrlr._Message)))
        self.assertEqual(l_msg[1], 0x62)
        self.assertEqual(self.m_ctrlr._Message[1], 0x50)


    def test_03_GetObjFromMsg(self):
        pass

def suite():
    suite = unittest.TestSuite()
    # suite.addTest(C01('test_01_FindAddress'))
    return suite

# ## END DBK
