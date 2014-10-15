"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Families/Insteon/test/test_Insteon_decoder.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jul 18, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files
# from Modules.lights.lighting import LightData
from Modules.Families.Insteon import Insteon_decoder
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')
MSG_99 = bytearray(b'\x02\x99')



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C01(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # PrettyPrintAny(self.m_pyhouse_obj.House.OBJs)
        self.m_controller_obj = self.m_pyhouse_obj.House.OBJs.Controllers
        self.m_api = Insteon_decoder.DecodeResponses(self.m_pyhouse_obj, self.m_controller_obj)


    def test_01_DeviceClass(self):
        pass

    def test_02_FindAddress(self):
        l_obj = self.m_api._find_addr(self.m_pyhouse_obj.House.OBJs.Controllers, 'A1.B2.C3')
        PrettyPrintAny(l_obj, 'testInsteonDecoder - FindAddress - Object', 120)


    def test_03_GetObjFromMsg(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(C01('test_01_FindAddress'))
    return suite

# ## END DBK
