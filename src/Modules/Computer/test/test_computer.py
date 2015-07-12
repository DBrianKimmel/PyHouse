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
        self.m_api = computer.API()


class C01_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml.root, 'XML')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer Division')
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'XML')

    def test_02_Update(self):
        self.m_api.update_data_structures(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')

    def test_03_Update(self):
        self.m_api.update_data_structures(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Computer')


class C02_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_api.update_data_structures(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        PrettyPrintAny(l_xml, 'XML')

    def test_02_Base(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_api.update_data_structures(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        self.m_api._read_computer_base_xml(l_xml)
        PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Computer')

    def test_03_All(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_api.update_data_structures(self.m_pyhouse_obj)
        l_computer = self.m_api.read_computer_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_computer, 'Computer')

class C03_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_api.update_data_structures(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        PrettyPrintAny(l_xml, 'XML')

    def test_02_Base(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_computer = self.m_api.read_computer_xml(self.m_pyhouse_obj)
        l_xml = self.m_api._write_computer_base_xml(l_computer)
        PrettyPrintAny(l_xml, 'Computer')

    def test_03_All(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_computer = self.m_api.read_computer_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer = l_computer
        l_xml = self.m_api.write_computer_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'Computer XML')

# # ## END DBK
