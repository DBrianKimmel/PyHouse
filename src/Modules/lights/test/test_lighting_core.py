"""
@name: PyHouse/src/Modules/lights/test/test_lighting_core.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 4, 2014
@summary: This module is for testing lighting Core.

Tests all working OK - DBK 2014-06-17
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseObjs, LightData, ControllerData
from Modules.lights.lighting_core import ReadWriteConfigXml
from Modules.families import family
from src.test import xml_data, test_mixin
from Modules.utils.tools import PrettyPrintAny

XML = xml_data.XML_LONG


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        PrettyPrintAny(self, 'TestLightingCore - SetupMixin - Self', 100)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        super(Test_02_XML, self).__init__()
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)
        self.m_pyhouse_obj = PyHouseData()

        self.m_api = ReadWriteConfigXml()

        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseObjs = HouseObjs()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml
        self.m_light_data = LightData()

        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_controller_sect_xml = self.m_house_div_xml.find('ControllerSection')
        self.m_controller_xml = self.m_controller_sect_xml.find('Controller')
        self.m_controller_obj = ControllerData()
        PrettyPrintAny(self, 'TestLightingCore - Test_02_Setup - Self', 100)

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_div_xml.tag, 'HouseDivision', 'XML - No Houses section')

    def test_0203_ReadBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_lighting_xml(self.m_light_data, self.m_light_xml)
        print('Controller: {0:}'.format(vars(l_base)))
        self.assertEqual(l_base.Name, 'Test LR Overhead', 'Bad Name')
        self.assertEqual(l_base.Key, 0, 'Bad Key')
        self.assertEqual(l_base.Active, True, 'Bad Active')
        self.assertEqual(l_base.Comment, 'SwitchLink On/Off', 'Bad Comments')
        self.assertEqual(l_base.Coords, "['0', '0']", 'Bad Coords')
        self.assertEqual(l_base.IsDimmable, False, 'Bad Dimmable')
        self.assertEqual(l_base.ControllerFamily, 'Insteon', 'Bad ControllerFamily')
        self.assertEqual(l_base.RoomName, 'Test Living Room', 'Bad Room Name')

    def test_0204_WriteBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_lighting_xml(self.m_light_data, self.m_light_xml)
        l_xml = self.m_api.write_base_lighting_xml(l_xml, l_base)
        PrettyPrintAny(l_xml, 'Lighting Core')

# ## END DBK
