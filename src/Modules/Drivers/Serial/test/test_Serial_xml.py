"""
@name:      PyHouse/src/Modules/Drivers/Serial/test/test_serial_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 5, 2014
@Summary:

Passed all 6 tests - DBK - 2015-07-30

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Drivers.Serial.Serial_xml import XML as serialXML
from Modules.Lighting.lighting_controllers import API as controllerAPI
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.xml_tools import stuff_new_attrs


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_controller_obj = ControllerData()
        self.m_controller_obj.InterfaceType = 'Serial'
        self.m_version = '1.4.0'


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        # self.m_pyhouse_obj.House.FamilyData = family.API(self.m_pyhouse_obj).build_lighting_family_info()

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass

    def test_02_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml, 'Xml')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_03_Controller(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_controller_obj, 'Controller')
        pass


class B1_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_controller_obj.InterfaceType = 'Serial'

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_02_ReadSerialXml(self):
        l_interface = serialXML.read_interface_xml(self.m_xml.controller)
        # PrettyPrintAny(l_interface, 'Read Interface', 100)
        self.assertEqual(l_interface.BaudRate, 19200, 'Bad Baud Rate')
        self.assertEqual(l_interface.ByteSize, 8, 'Bad ByteSize')
        self.assertEqual(l_interface.DsrDtr, False, 'Bad DsrDtr')
        self.assertEqual(l_interface.Parity, 'N', 'Bad Parity')
        self.assertEqual(l_interface.RtsCts, False, 'Bad RtsCts')
        self.assertEqual(l_interface.StopBits, 1.0, 'Bad StopBits')
        self.assertEqual(l_interface.Timeout, 1.0, 'Bad Timeout')
        self.assertEqual(l_interface.XonXoff, False, 'Bad XonXoff')


class B2_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_WriteSerialXml(self):
        l_interface = serialXML.read_interface_xml(self.m_xml.controller)
        stuff_new_attrs(self.m_controller_obj, l_interface)
        # PrettyPrintAny(self.m_controller_obj, 'Controller', 120)
        l_xml = ET.Element('TestOutput')
        l_xml = serialXML.write_interface_xml(l_xml, self.m_controller_obj)
        # PrettyPrintAny(l_xml, 'Interface Xml', 120)

# ## END
