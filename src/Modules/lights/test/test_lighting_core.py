"""
@name: PyHouse/src/Modules/lights/test/test_lighting_core.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 4, 2014
@summary: This module is for testing lighting Core.

Tests all working OK - DBK 2014-07-27
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.lights.lighting_core import ReadWriteConfigXml
from Modules.families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.utils.tools import PrettyPrintAny

XML = xml_data.XML_LONG


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
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = ReadWriteConfigXml()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_obj.Xml', 120)

    def test_0203_ReadBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.light)
        PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'outside_front', 'Bad Name')
        self.assertEqual(l_base.Key, 0, 'Bad Key')
        self.assertEqual(l_base.Active, True, 'Bad Active')
        self.assertEqual(l_base.Comment, 'SwitchLink On/Off', 'Bad Comments')
        self.assertEqual(l_base.Coords, "['0', '0']", 'Bad Coords')
        self.assertEqual(l_base.IsDimmable, False, 'Bad Dimmable')
        self.assertEqual(l_base.ControllerFamily, 'Insteon', 'Bad ControllerFamily')
        self.assertEqual(l_base.RoomName, 'Foyer', 'Bad Room Name')

    def test_0204_WriteBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.light)
        l_xml = self.m_api.write_base_lighting_xml(l_base)
        PrettyPrintAny(l_xml, 'Lighting Core')


class Test_03_EmptyXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_EMPTY)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = ReadWriteConfigXml()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_obj.Xml', 120)

    def test_0203_ReadBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.light)
        PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, None, 'Bad Name')
        self.assertEqual(l_base.Key, None, 'Bad Key')
        self.assertEqual(l_base.Active, False, 'Bad Active')
        self.assertEqual(l_base.Comment, None, 'Bad Comments')
        self.assertEqual(l_base.Coords, None, 'Bad Coords')
        self.assertEqual(l_base.IsDimmable, False, 'Bad Dimmable')
        self.assertEqual(l_base.ControllerFamily, None, 'Bad ControllerFamily')
        self.assertEqual(l_base.RoomName, None, 'Bad Room Name')

    def test_0204_WriteBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_xml = self.m_api.write_base_lighting_xml(self.m_light_obj)
        PrettyPrintAny(l_xml, 'Lighting Core')

# ## END DBK
