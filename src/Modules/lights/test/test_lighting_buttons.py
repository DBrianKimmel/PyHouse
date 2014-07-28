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
from Modules.Core.data_objects import PyHouseData, ButtonData
from Modules.lights import lighting_buttons
from Modules.families import family
from Modules.web import web_utils
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data, test_mixin

class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_button_sect_xml = self.m_house_div_xml.find('ButtonSection')
        self.m_button_xml = self.m_button_sect_xml.find('Button')
        self.m_light_obj = ButtonData()

        self.m_api = lighting_buttons.ButtonsAPI(self.m_pyhouse_obj)

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_div_xml.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_button_sect_xml.tag, 'ButtonSection', 'XML - No Buttons section')
        self.assertEqual(self.m_button_xml.tag, 'Button', 'XML - No Button section')

    def test_0203_ReadOneButtonXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_button = self.m_api.read_one_button_xml(self.m_button_xml)
        self.assertEqual(l_button.Active, False, 'Bad Active')
        self.assertEqual(l_button.Key, 0, 'Bad key')
        self.assertEqual(l_button.Name, 'kpl_1_A', 'Bad Name')
        PrettyPrintAny(l_button, 'ReadOneButton', 120)

    def test_0204_ReadAllButtonsXml(self):
        l_buttons = self.m_api.read_buttons_xml(self.m_button_sect_xml)
        self.assertEqual(len(l_buttons), 4)
        PrettyPrintAny(l_buttons, 'ReadAllButton', 120)

    def test_0211_WriteOneButtonXml(self):
        """ Write out the XML file for the button section
        """
        l_button = self.m_api.read_one_button_xml(self.m_button_xml)
        l_xml = self.m_api.write_one_button_xml(l_button)
        print('XML: {0:}'.format(PrettyPrintAny(l_xml)))

    def test_0212_WriteAllButtonsXml(self):
        """ Write out the XML file for the Buttons section
        """
        l_button = self.m_api.read_buttons_xml(self.m_button_sect_xml)
        l_xml = self.m_api.write_buttons_xml(l_button)
        print('XML: {0:}'.format(PrettyPrintAny(l_xml)))

    def test_0221_CreateJson(self):
        """ Create a JSON object for Buttons.
        """
        l_buttons = self.m_api.read_buttons_xml(self.m_button_sect_xml)
        print('ButtonsS: {0:}'.format(l_buttons))
        print('Button 0: {0:}'.format(vars(l_buttons[0])))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_buttons))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
