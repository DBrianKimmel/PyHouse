"""
@name: PyHouse/src/Modules/families/Insteon/test/test_Device_Insteon.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: This module is for testing lighting Core.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, LightData
from Modules.families.Insteon import Device_Insteon
from Modules.lights import lighting_lights
from src.test import xml_data
from Modules.utils.tools import PrettyPrintAny

XML = xml_data.XML_LONG


class Test_02_ReadXML(unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.House.OBJs = {}
        self.m_pyhouse_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses_xml = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_lights_xml = self.m_house_xml.find('Lights')
        self.m_light_xml = self.m_lights_xml.find('Light')
        self.m_api = Device_Insteon.API()
        self.m_device_obj = LightData()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_light_xml.tag, 'Light', 'XML - No Light section')

    def test_0203_ReadOneLightXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_light = lighting_lights.LightingLightsAPI().read_one_light_xml(self.m_light_xml)
        l_insteon_obj = self.m_api.extract_device_xml(l_light, self.m_light_xml)
        PrettyPrintAny(l_insteon_obj)
        self.assertEqual(l_light.Name, 'Test LR Overhead', 'Bad Name')
        self.assertEqual(l_light.Key, 0, 'Bad Key')
        self.assertEqual(l_light.Active, True, 'Bad Active')
        self.assertEqual(l_light.UUID, 'ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2', 'Bad UUID')
        self.assertEqual(l_light.InsteonAddress, 1122867, 'Bad Address')
        self.assertEqual(l_light.DevCat, '3140', 'Bad DevCat')
        self.assertEqual(l_light.ProductKey, '30.1A.35', 'Bad ProductKey')

# ## END
