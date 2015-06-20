"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@note:      Created on Apr 9, 2013
@license:   MIT License
@summary:   Handle the home lighting system automation.

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Lighting import lighting
from Modules.Families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C01_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = lighting.API()

    def test_01_SetUp(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_xml, 'Tags')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')

    def test_02_Read(self):
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'PyHouse_obj.House.DeviceOBJs')
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Lights[0].Name, 'Insteon Light')

    def test_03_Write(self):
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        l_obj = self.m_pyhouse_obj.House.DeviceOBJs
        l_xml = ET.Element('HouseDivision')
        PrettyPrintAny(l_obj, 'Lighting')
        self.m_api._write_lighting_xml(l_obj, l_xml)
        PrettyPrintAny(l_xml, 'XML')



class C02_Utility(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = lighting.API()

    def test_01_FindFull(self):
        l_web_obj = LightData()
        l_web_obj.Name = 'dr_chand'
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        l_light = self.m_api._find_full_obj(self.m_pyhouse_obj.House.DeviceOBJs.Lights, l_web_obj)
        PrettyPrintAny(l_light, 'Light')
        self.assertEqual(l_light.Name, 'dr_chand')
        #
        l_web_obj.Name = 'NoSuchLight'
        l_light = self.m_api._find_full_obj(self.m_pyhouse_obj.House.DeviceOBJs.Lights, l_web_obj)
        self.assertEqual(l_light, None)


class C_03_Ops(SetupMixin, unittest.TestCase):
    """ This section tests the operations
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = lighting.API()

    def test_01_GetApi(self):
        l_light = self.m_light_obj
        l_light.Name = 'Garage'
        l_light.ControllerFamily = 'Insteon'
        l_api = self.m_api._get_api_for_family(self.m_pyhouse_obj, self.m_light_obj)
        print('Api = {0:}'.format(l_api))

# ## END DBK
