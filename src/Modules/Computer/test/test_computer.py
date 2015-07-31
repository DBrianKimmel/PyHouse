"""
@name:      PyHouse/src/Modules/Computer/test/test_computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 25, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Computer import computer
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = computer.API(self.m_pyhouse_obj)


class C01_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml.root, 'XML')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer Division')
        # PrettyPrintAny(self.m_pyhouse_obj.Xml, 'XML')


class C02_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        # PrettyPrintAny(l_xml, 'XML')


class C03_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        # PrettyPrintAny(l_xml, 'XML')

# # ## END DBK
