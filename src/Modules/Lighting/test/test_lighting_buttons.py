"""
@name: PyHouse/src/Modules/lighting/test/test_lighting_buttons.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 22, 2014
@summary: This module is for testing lighting buttons data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ButtonData
from Modules.Lighting import lighting_buttons
from Modules.Families import family
from Modules.Core import conversions
from Modules.Web import web_utils
from test.xml_data import *
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = lighting_buttons.LBApi(self.m_pyhouse_obj)
        self.m_controller_obj = ButtonData()

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection', 'XML - No Buttons section')
        self.assertEqual(self.m_xml.button.tag, 'Button', 'XML - No Button section')

    def test_0211_ReadButtonData(self):
        """ Read in the xml file and fill in the lights
        """
        l_button = self.m_api._read_button_data(self.m_xml.button)
        PrettyPrintAny(l_button, 'ButtonData', 120)
        self.assertEqual(l_button.Name, 'kpl_1_A', 'Bad Name')
        self.assertEqual(l_button.Active, False, 'Bad Active')
        self.assertEqual(l_button.Comment, 'KeypadLink Button A', 'Bad Comment')
        self.assertEqual(l_button.ControllerFamily, 'Insteon', 'Bad Controller Family')
        self.assertEqual(l_button.LightingType, 'Button', 'Bad Lighting Type')
        self.assertEqual(l_button.RoomName, 'Master Bath', 'Bad Room Name')

    def test_0213_ReadOneButtonXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_button = self.m_api.read_one_button_xml(self.m_xml.button)
        PrettyPrintAny(l_button, 'ReadOneButton', 120)
        self.assertEqual(l_button.Name, 'kpl_1_A', 'Bad Name')
        self.assertEqual(l_button.Active, False, 'Bad Active')
        self.assertEqual(l_button.Key, 0, 'Bad key')
        self.assertEqual(l_button.Name, 'kpl_1_A', 'Bad Name')
        self.assertEqual(l_button.ControllerFamily, 'Insteon', 'Bad Lighting family')
        self.assertEqual(l_button.LightingType, 'Button', 'Bad LightingType')
        self.assertEqual(l_button.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))

    def test_0215_ReadAllButtonsXml(self):
        l_buttons = self.m_api.read_all_buttons_xml(self.m_xml.button_sect)
        self.assertEqual(len(l_buttons), 4)
        PrettyPrintAny(l_buttons, 'ReadAllButton', 120)

    def test_0231_WriteOneButtonXml(self):
        """ Write out the XML file for the button section
        """
        l_button = self.m_api.read_one_button_xml(self.m_xml.button)
        l_xml = self.m_api.write_one_button_xml(l_button)
        print('XML: {0:}'.format(PrettyPrintAny(l_xml)))

    def test_0232_WriteAllButtonsXml(self):
        """ Write out the XML file for the Buttons section
        """
        l_button = self.m_api.read_all_buttons_xml(self.m_xml.button_sect)
        l_xml = self.m_api.write_buttons_xml(l_button)
        print('XML: {0:}'.format(PrettyPrintAny(l_xml)))

    def test_0251_CreateJson(self):
        """ Create a JSON object for Buttons.
        """
        l_buttons = self.m_api.read_all_buttons_xml(self.m_xml.button_sect)
        print('ButtonsS: {0:}'.format(l_buttons))
        print('Button 0: {0:}'.format(vars(l_buttons[0])))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_buttons))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
