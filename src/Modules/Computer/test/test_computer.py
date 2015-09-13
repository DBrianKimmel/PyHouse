"""
@name:      PyHouse/src/Modules/Computer/test/test_computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 25, 2014
@Summary:

Passed all 3 tests - DBK - 2015-09-12

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Computer.computer import API as computerAPI, Xml as computerXML
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny

DIVISION = 'ComputerDivision'
MQTT_SECTION = 'MqttSection'

class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = computerAPI(self.m_pyhouse_obj)


class C01_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        Test some scattered things so we don't end up with hundreds of asserts.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, DIVISION)
        self.assertEqual(self.m_xml.mqtt_sect.tag, MQTT_SECTION)


class C2_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Xml(self):
        """ Read the config - it is minimal.
        """
        l_xml = computerXML.read_computer_xml(self.m_pyhouse_obj)
        self.assertEqual(l_xml.tag, DIVISION)
        l_mqtt = l_xml.find(MQTT_SECTION)
        self.assertNotEqual(l_mqtt, None)


class C3_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = computerXML.read_computer_xml(self.m_pyhouse_obj)
        l_mqtt = l_xml.find(MQTT_SECTION)
        # PrettyPrintAny(l_mqtt, 'XML')
        self.assertNotEqual(l_mqtt, None)

# # ## END DBK
