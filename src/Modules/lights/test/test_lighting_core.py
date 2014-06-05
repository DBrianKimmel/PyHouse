"""
@name: PyHouse/src/Modules/lights/test/test_lighting_core.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 4, 2014
@summary: This module is for testing lighting Core.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseData
from Modules.lights import lighting_core
from src.test import xml_data

XML = xml_data.XML_LONG


class Test_02_ReadXML(unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses_xml = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_controllers_xml = self.m_house_xml.find('Controllers')
        self.m_controller_xml = self.m_controllers_xml.find('Controller')
        self.m_api = lighting_core.CoreAPI()

    def tXest_0201_list_elements(self):
        l_list = self.m_house_xml.iter()
        for l_tag in l_list:
            print(' Elements: {0:}  Items: {1:}'.format(l_tag.tag, l_tag.items()))

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')

    def test_0203_ReadOneControllerXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_controller_xml)
        print('Controller: {0:}'.format(vars(l_controller)))
        self.assertEqual(l_controller.Name, 'PLM_1', 'Bad Name')
        self.assertEqual(l_controller.Key, 0, 'Bad Key')
        self.assertEqual(l_controller.Active, False, 'Bad Active')
        self.assertEqual(l_controller.Comment, 'Dongle using serial converter 067B:2303', 'Bad Comments')
        self.assertEqual(l_controller.Coords, 'None', 'Bad Coords')
        self.assertEqual(l_controller.Dimmable, True, 'Bad Dimmable')
        self.assertEqual(l_controller.Family, 'Insteon', 'Bad Family')
        self.assertEqual(l_controller.Interface, 'Serial', 'Bad Interface')
        self.assertEqual(l_controller.RoomName, 'Office', 'Bad Room Name')
        self.assertEqual(l_controller.Type, 'Controller', 'Bad Type')

# ## END DBK
