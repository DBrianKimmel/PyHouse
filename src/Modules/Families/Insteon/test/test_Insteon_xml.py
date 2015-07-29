"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Aug 5, 2014
@license:   MIT License
@summary:   This module test insteon xml

Passed all 13 tests - DBK - 2015-07-20
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData, HouseInformation
from Modules.Core.test.xml_device import TESTING_DEVICE_FAMILY
from Modules.Families.Insteon.Insteon_xml import API as InsteonXmlAPI
from Modules.Core import conversions
from Modules.Lighting.lighting_core import API as lightingCoreAPI
from test.xml_data import XML_LONG
from Modules.Lighting.test.xml_lights import TESTING_LIGHTING_LIGHTS_INSTEON_NAME
from Modules.Families.Insteon.test.xml_insteon import \
        TESTING_INSTEON_ADDRESS, \
        TESTING_INSTEON_DEVCAT, \
        TESTING_INSTEON_GROUP_LIST, \
        TESTING_INSTEON_GROUP_NUM, \
        TESTING_INSTEON_MASTER, \
        TESTING_INSTEON_PRODUCT_KEY
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):
    """ Set up pyhouse object
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = InsteonXmlAPI
        self.m_core_api = lightingCoreAPI()
        self.m_device = LightData()
        self.m_version = '1.4.0'


class A1_Prep(SetupMixin, unittest.TestCase):
    """ This section tests the setup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device = None

    def test_01_PyHouse(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'InsteonXML PyHouse')
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)

    def test_02_Computer(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Computer')

    def test_03_House(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj.House, 'House')

    def test_04_Objs(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'DeviceOBJs')

    def test_05_XML(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_xml, 'XML')

    def test_06_Device(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_device, 'XML Device')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controller section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No controller Entry')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ProductKey(self):
        l_product_key = InsteonXmlAPI._read_product_key(self.m_xml.light)
        print('ProductKey: {}'.format(conversions.int2dotted_hex(l_product_key, 3)))
        self.assertEqual(conversions.int2dotted_hex(l_product_key, 3), TESTING_INSTEON_PRODUCT_KEY)

    def test_02_Insteon(self):
        l_insteon = InsteonXmlAPI._read_insteon(self.m_xml.light)
        PrettyPrintAny(l_insteon, 'Insteon')
        self.assertEqual(conversions.int2dotted_hex(l_insteon.InsteonAddress, 3), TESTING_INSTEON_ADDRESS)
        self.assertEqual(conversions.int2dotted_hex(l_insteon.DevCat, 2), TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_insteon.GroupList, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_insteon.GroupNumber, int(TESTING_INSTEON_GROUP_NUM))
        self.assertEqual(l_insteon.IsMaster, conversions.getbool(TESTING_INSTEON_MASTER))
        self.assertEqual(conversions.int2dotted_hex(l_insteon.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY)

    def test_03_Core(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light, self.m_version)
        PrettyPrintAny(l_light, 'Light')
        PrettyPrintAny(self.m_device, 'Device')
        self.assertEqual(l_light.Name, TESTING_LIGHTING_LIGHTS_INSTEON_NAME)
        self.assertEqual(l_light.DeviceFamily, 'Insteon')

    def test_04_InsteonLight(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light, self.m_version)
        l_ret = self.m_api.ReadXml(l_light, self.m_xml.light)
        PrettyPrintAny(l_ret, 'Lret')
        PrettyPrintAny(l_light, 'Light Device 2')
        self.assertEqual(l_light.Name, TESTING_LIGHTING_LIGHTS_INSTEON_NAME)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))


class C01_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_setup(self):
        PrettyPrintAny(self.m_xml.light, 'XML')

    def test_02_Core(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light, self.m_version)
        l_xml = self.m_core_api.write_base_lighting_xml('Light', l_light)
        PrettyPrintAny(l_xml, 'Lights XML')

    def test_03_InsteonLight(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light, self.m_version)
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
