"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Families/Insteon/test/test_Insteon_decoder.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com>
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
from Modules.Housing import house
from Modules.Utilities.tools import PrettyPrintAny
from Modules.Core import setup
from test import xml_data


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = setup.build_pyhouse_obj(self)
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        #
        self.m_api = Insteon_decoder.Utility()
        self.m_house_api = house.API()
        self.m_pyhouse_obj = self.m_house_api.update_pyhouse_obj(self.m_pyhouse_obj)
        return self.m_pyhouse_obj


class Test_01(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

    def test_0101_FindAddress(self):
        # l_obj = self.m_api._find_addr(self.m_pyhouse_obj.House.OBJs.Controllers, 'A1.B2.C3')
        # PrettyPrintAny(l_obj, 'testInsteonDecoder - FindAddress - Object', 120)
        pass

    def test_0102_x(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_01('test_0101_FindAddress'))
    return suite

# ## END DBK
