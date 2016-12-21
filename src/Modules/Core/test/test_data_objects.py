"""
@name:      PyHouse/src/Modules/Core/test/test_data_objects.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gm6il.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Mar 22, 2014
@license:   MIT License
@summary:   test ?.

Passed all 4 tests - DBK - 2016-11-14

"""
from Modules.Housing.test.xml_housing import TESTING_HOUSE_NAME
from Modules.Housing.test.xml_location import TESTING_LOCATION_STREET

__updated__ = '2016-11-14'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core import data_objects
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_data_objects')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-1-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.node_sect.tag, 'NodeSection')
        self.assertEqual(self.m_xml.node.tag, 'Node')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')

    def test_02_name(self):
        l_house = self.m_pyhouse_obj.House
        l_name = l_house.Name
        self.assertEqual(l_name, TESTING_HOUSE_NAME)

    def test_03_street(self):
        l_data = self.m_pyhouse_obj
        l_house = l_data.House
        l_location = l_house.Location
        l_street = l_location.Street
        self.assertEqual(l_street, TESTING_LOCATION_STREET)

# ## END DBK
