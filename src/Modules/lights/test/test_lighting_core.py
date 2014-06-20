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
from Modules.Core.data_objects import PyHouseData, HouseData, LightData
from Modules.lights import lighting_core
from src.test import xml_data
from Modules.utils.tools import PrettyPrintAny

XML = xml_data.XML_LONG


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_api = lighting_core.LightingCoreAPI()

        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml
        self.m_light_data = LightData()

        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')

        self.m_lights_xml = self.m_house_xml.find('Lights')
        self.m_light_xml = self.m_lights_xml.find('Light')
        # print('SetupMixin setUp ran')


class Test_02_ReadXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)
        self.m_pyhouse_obj = PyHouseData()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')

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
        self.assertEqual(l_base.Dimmable, False, 'Bad Dimmable')
        self.assertEqual(l_base.LightingFamily, 'Insteon', 'Bad LightingFamily')
        self.assertEqual(l_base.RoomName, 'Test Living Room', 'Bad Room Name')

    def test_0204_WriteBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_lighting_xml(self.m_light_data, self.m_light_xml)
        l_xml = self.m_api.write_base_lighting_xml(l_xml, l_base)
        PrettyPrintAny(l_xml, 'Lighting Core')

# ## END DBK
