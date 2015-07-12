"""
@name:      PyHouse/src/Modules/Families/test/test_family_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014_2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 15, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Core import conversions
from Modules.Families.family import API as familyAPI
from Modules.Families.family_utils import FamUtil
from Modules.Lighting.lighting_core import LightingCoreXmlAPI
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = familyAPI(self.m_pyhouse_obj).m_family
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_device_obj = LightData()
        self.m_device_obj.Name = 'Testing Device'
        self.m_device_obj.DeviceFamily = 'Insteon'
        self.m_device_obj.Active = True
        self.m_device_obj.DeviceType = 1
        self.m_device_obj.DeviceSubType = 234


class A1_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Setup(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs, 'RefOBJs', 115)
        PrettyPrintAny(self.m_xml, 'XML')
        # self.assertEqual(len(VALID_FAMILIES), len(self.m_pyhouse_obj.House.RefOBJs.FamilyData))

    def test_02_Device(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_device_obj, 'Device')
        # self.assertEqual(len(VALID_FAMILIES), len(self.m_pyhouse_obj.House.RefOBJs.FamilyData))

    def test_03_Families(self):
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.FamilyData, 'Families')

    def test_04_Family(self):
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.FamilyData['Insteon'], 'Families')


class B1_Utils(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_GetDeviceName(self):
        l_device = FamUtil._get_device_name(self.m_device_obj)
        print('Device Name: {}'.format(l_device))
        self.assertEqual(l_device, 'Testing Device')

    def test_02_GetFamilyName(self):
        l_name = FamUtil._get_family_name(self.m_device_obj)
        print('Family Name: {}'.format(l_name))
        self.assertEqual(l_name, 'Insteon')

    def test_03_GetFamilyObj(self):
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        PrettyPrintAny(l_obj, 'Family')
        self.assertEqual(l_obj.Name, 'Insteon')

    def test_04_GetInsteon(self):
        """ Did we get a family?
        """
        l_family = FamUtil.get_family(self.m_device_obj)
        PrettyPrintAny(self.m_device_obj, 'Device')
        print('Testing - Family: "{}"'.format(l_family))
        self.assertEqual(l_family, 'Insteon')

    def test_05_GetUPB(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        self.m_device_obj.DeviceFamily = 'UPB'
        l_family = FamUtil.get_family(self.m_device_obj)
        PrettyPrintAny(self.m_device_obj, 'Device')
        print('Testing - Family: "{}"'.format(l_family))
        self.assertEqual(l_family, 'UPB')

    def test_06_GetApi(self):
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        PrettyPrintAny(l_api, 'API')
        self.assertNotEqual(l_api, None)


class C1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj.DeviceFamily = 'Insteon'
        self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)

    def test_01_Print(self):
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs, 'Ref Objs')
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.FamilyData['Insteon'], 'Insteon Family Data')
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.FamilyData['Insteon'].FamilyModuleAPI, '')

    def test_02_Xml(self):
        """ Did we get the XML correctly
        """
        l_xml = self.m_xml.light
        PrettyPrintAny(l_xml, 'XML')

    def test_03_Device(self):
        """ Did we get the Device correctly
        """
        l_device = self.m_device_obj
        PrettyPrintAny(l_device, 'Device')
        self.assertEqual(l_device.Name, 'Testing Device')
        self.assertEqual(l_device.Key, 0)
        self.assertEqual(l_device.Active, True)
        self.assertEqual(l_device.DeviceFamily, 'Insteon')
        self.assertEqual(l_device.DeviceType, 1)
        self.assertEqual(l_device.DeviceSubType, 234)
        self.assertEqual(l_device.RoomName, '')

    def test_04_Family(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = FamUtil.read_family_data(self.m_pyhouse_obj, l_device, l_xml)
        PrettyPrintAny(l_light, 'Light')

    def test_05_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = LightingCoreXmlAPI().read_core_lighting_xml(l_device, l_xml)
        PrettyPrintAny(l_light, 'Light')
        self.assertEqual(l_light.Name, 'Insteon Light')
        self.assertEqual(l_device.RoomName, 'Master Bath')

    def test_06_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        #
        l_light = LightingCoreXmlAPI().read_core_lighting_xml(l_device, l_xml)
        PrettyPrintAny(l_light, 'Light w/o family data')
        FamUtil.read_family_data(self.m_pyhouse_obj, l_light, l_xml)
        PrettyPrintAny(l_light, 'Light w/ family Data')
        self.assertEqual(l_light.Name, 'Insteon Light')
        self.assertEqual(l_light.DeviceFamily, 'Insteon')
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int('16.62.2D'))
        self.assertEqual(l_light.DevCat, conversions.dotted_hex2int('02.1C'))
        self.assertEqual(l_light.ProductKey, conversions.dotted_hex2int('30.1A.35'))


class D1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj.DeviceFamily = 'Insteon'
        self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        self.m_light = LightingCoreXmlAPI().read_core_lighting_xml(self.m_device_obj, self.m_xml.controller)

    def test_01_Data(self):
        PrettyPrintAny(self.m_light, 'Light Dtaa')

    def test_03_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_in_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = LightingCoreXmlAPI().read_core_lighting_xml(l_device, l_in_xml)
        FamUtil.read_family_data(self.m_pyhouse_obj, l_light, l_in_xml)

        l_out_xml = LightingCoreXmlAPI().write_base_lighting_xml('Light', l_light)
        PrettyPrintAny(l_out_xml, 'xml 1')
        FamUtil.write_family_data(self.m_pyhouse_obj, l_out_xml, l_light)
        PrettyPrintAny(l_out_xml, 'xml 2')

        self.assertEqual(l_light.Name, 'Insteon Light')
        self.assertEqual(l_light.DeviceFamily, 'Insteon')
        self.assertEqual(l_light.InsteonAddress, 1466925)

# ## END DBK
