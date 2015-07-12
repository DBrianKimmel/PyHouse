"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Aug 5, 2014
@license:   MIT License
@summary:   This module test insteon xml

Passed all 4 tests - DBK - 2014-07-18
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Families.Insteon import Insteon_xml
from Modules.Core import conversions
from Modules.Lighting import lighting_core
from test.xml_data import *
from Modules.Lighting.test.xml_lights import TESTING_LIGHTING_LIGHTS_INSTEON_NAME
from Modules.Families.Insteon.test.xml_insteon import TESTING_INSTEON_ADDRESS
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = Insteon_xml.API(self.m_pyhouse_obj)
        self.m_core_api = lighting_core.LightingCoreXmlAPI()
        self.m_device = LightData()


class A1_Prep(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device = None

    def test_01_Setup(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Computer')
        PrettyPrintAny(self.m_pyhouse_obj.House, 'House')

    def test_02_Setup(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'DeviceOBJs')
        PrettyPrintAny(self.m_xml, 'XML')
    def test_03_Setup(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'DeviceOBJs')
        PrettyPrintAny(self.m_xml, 'XML')

    def test_04_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_xml, 'XML')
        PrettyPrintAny(self.m_device, 'XML Device')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controller section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No controller Entry')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_setup(self):
        PrettyPrintAny(self.m_xml.light, 'XML')
        PrettyPrintAny(self.m_device, 'Light Device')

    def test_02_Core(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light)
        PrettyPrintAny(l_light, 'Light')
        PrettyPrintAny(self.m_device, 'Device')
        self.assertEqual(l_light.Name, TESTING_LIGHTING_LIGHTS_INSTEON_NAME)
        self.assertEqual(l_light.DeviceFamily, 'Insteon')

    def test_03_InsteonLight(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light)
        l_ret = self.m_api.ReadXml(l_light, self.m_xml.light)
        PrettyPrintAny(l_ret, 'Lret')
        PrettyPrintAny(l_light, 'Light Device 2')
        self.assertEqual(l_light.Name, TESTING_LIGHTING_LIGHTS_INSTEON_NAME)
        self.assertEqual(l_light.DeviceFamily, 'Insteon')
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))


class C01_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_setup(self):
        PrettyPrintAny(self.m_xml.light, 'XML')

    def test_02_Core(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light)
        l_xml = self.m_core_api.write_base_lighting_xml('Light', l_light)
        PrettyPrintAny(l_xml, 'Lights XML')

    def test_03_InsteonLight(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light)
        self.m_api.ReadXml(l_light, self.m_xml.light)
        PrettyPrintAny(l_light, 'Light Device 2')
        l_xml = self.m_core_api.write_base_lighting_xml('Light', l_light)
        # self.m_api.SaveXml(l_xml, l_light)
        PrettyPrintAny(l_xml, 'Lights XML')


def test_suite():
    suite = unittest.TestSuite()
    # suite.addTests(XML())
    return suite

# ## END
