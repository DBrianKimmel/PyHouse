"""
@name:      PyHouse/src/Modules/Core/test/test_data_objects.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gm6il.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@note:      Created on Mar 22, 2014
@license:   MIT License
@summary:   test ?.

Passed all 2 tests - DBK - 2017-01-19

"""

__updated__ = '2017-01-19'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_DIVISION
from Modules.Housing.Lighting.test.xml_lighting import \
    TESTING_LIGHTING_SECTION
from Modules.Computer.test.xml_computer import \
    TESTING_COMPUTER_DIVISION
from Modules.Computer.Nodes.test.xml_nodes import \
    TESTING_NODE_SECTION
from Modules.Housing.Lighting.test.xml_buttons import \
    TESTING_BUTTON_SECTION, \
    TESTING_BUTTON


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
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)
        self.assertEqual(self.m_xml.node_sect.tag, TESTING_NODE_SECTION)
        self.assertEqual(self.m_xml.node.tag, 'Node')
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.lighting_sect.tag, TESTING_LIGHTING_SECTION)
        self.assertEqual(self.m_xml.button_sect.tag, TESTING_BUTTON_SECTION)
        self.assertEqual(self.m_xml.button.tag, TESTING_BUTTON)

# ## END DBK
