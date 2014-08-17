"""
@name: PyHouse/src/Modules/families/Insteon/test/test_Insteon_xml.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Aug 5, 2014
@license: MIT License
@summary: This module test insteon xml

Passed all 4 tests - DBK - 2014-07-18
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData, LightData
from Modules.Families.Insteon import Insteon_xml
from Modules.Core import conversions
from Modules.Lighting import lighting_controllers
from Modules.Lighting.lighting_core import ReadWriteConfigXml
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = Insteon_xml.ReadWriteConfigXml()
        self.m_controller_api = lighting_controllers.ControllersAPI(self.m_pyhouse_obj)

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controller section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No controller Entry')
        print('Find XML')

    def test_0203_ReadOneControllerXml(self):
        """ Read in the xml file and fill in the lights
        """
        PrettyPrintAny(self.m_xml.controller, 'XML Controller', 120)
        l_device = LightData()
        # l_device = ReadWriteConfigXml().read_base_lighting_xml(l_device, self.m_xml.controller)
        l_device = self.m_controller_api._read_controller_data(self.m_xml.controller)
        self.m_api.ReadXml(l_device, self.m_xml.controller)
        PrettyPrintAny(l_device, 'Insteon', 120)
        self.assertEqual(l_device.Name, 'PLM_1', 'Bad Name')
        self.assertEqual(l_device.Key, 0, 'Bad Key')
        self.assertEqual(l_device.Active, False, 'Bad Active')
        self.assertEqual(l_device.InsteonAddress, conversions.dotted_hex2int('AA.AA.AA'), 'Bad Address')
        self.assertEqual(l_device.DevCat, conversions.dotted_hex2int('12.34'), 'Bad DevCat')
        self.assertEqual(l_device.ProductKey, conversions.dotted_hex2int('23.45.67'), 'Bad ProductKey')

def suite():
    suite = unittest.TestSuite()
    suite.addTests(Test_02_XML())
    # suite.addTest(Test_02_XML('test_0203_ReadOneControllerXml'))
    return suite

# ## END
