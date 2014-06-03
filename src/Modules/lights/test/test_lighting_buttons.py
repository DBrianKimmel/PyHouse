"""
@name: PyHouse/src/Modules/lighting/test/test_lighting_buttons.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 22, 2014
@summary: This module is for testing lighting buttons data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHousesData, HousesData, HouseData
from Modules.lights import lighting_buttons
from Modules.web import web_utils
from Modules.utils.xml_tools import PrettifyXML
from src.test import xml_data

XML = xml_data.XML_LONG


class Test_02_XML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses_xml = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_buttons_xml = self.m_house_xml.find('Buttons')
        self.m_button_xml = self.m_buttons_xml.find('Button')
        self.m_api = lighting_buttons.ButtonsAPI()

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_buttons_xml.tag, 'Buttons', 'XML - No Buttons section')
        self.assertEqual(self.m_button_xml.tag, 'Button', 'XML - No Button section')

    def test_0203_ReadOneButtonXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_button = self.m_api.read_one_button_xml(self.m_button_xml)
        print('Button: {0:}'.format(vars(l_button)))
        self.assertEqual(l_button.Active, False, 'Bad Active')
        self.assertEqual(l_button.Key, 0, 'Bad key')
        self.assertEqual(l_button.Name, 'kpl_1_A', 'Bad Name')

    def test_0204_ReadButtonsXml(self):
        l_buttons = self.m_api.read_buttons_xml(self.m_house_xml)
        print('Controllers {0:}'.format(l_buttons))
        self.assertEqual(len(l_buttons), 2)

    def test_0211_WriteOneButtonXml(self):
        """ Write out the XML file for the button section
        """
        l_button = self.m_api.read_one_button_xml(self.m_button_xml)
        l_xml = self.m_api.write_one_button_xml(l_button)
        print('XML: {0:}'.format(PrettifyXML(l_xml)))

    def test_0212_WriteButtonsXml(self):
        """ Write out the XML file for the Buttons section
        """
        l_button = self.m_api.read_buttons_xml(self.m_house_xml)
        l_xml = self.m_api.write_buttons_xml(l_button)
        print('XML: {0:}'.format(PrettifyXML(l_xml)))

    def test_0221_CreateJson(self):
        """ Create a JSON object for Buttons.
        """
        l_buttons = self.m_api.read_buttons_xml(self.m_house_xml)
        print('ButtonsS: {0:}'.format(l_buttons))
        print('Button 0: {0:}'.format(vars(l_buttons[0])))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_buttons))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
