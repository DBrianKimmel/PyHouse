"""
@name:      PyHouse/src/Modules/Drivers/test/test_interface.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   This module is for testing driver interface data.

Passed all 10 tests - DBK - 2018-03-13
"""

__updated__ = '2018-02-13'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import ControllerData
from Modules.Drivers.interface import Xml as interfaceXml
from Modules.Housing.Lighting.lighting_controllers import API as controllerAPI
from Modules.Drivers.Serial.test.xml_serial import XML_SERIAL
from Modules.Drivers.USB.test.xml_usb import XML_USB
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_controller_obj = ControllerData()
        self.m_ctlr_api = controllerAPI()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_interface')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_SERIAL
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:8], '<Serial>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_SERIAL)
        # print('A2-02-A - Parsed\n', l_xml)
        self.assertEqual(l_xml.tag, "Serial")

    def test_03_Raw(self):
        l_raw = XML_USB
        # print('A2-03-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:5], '<USB>')

    def test_04_Parsed(self):
        l_xml = ET.fromstring(XML_USB)
        # print('A2-04-A - Parsed\n', l_xml)
        self.assertEqual(l_xml.tag, "USB")


class A3_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        # sprint(PrettyFormatAny.form(self.m_root_xml, 'A3-01-A - Entire Xml'))
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        # print(PrettyFormatAny.form(self.m_xml.controller_sect, 'A3-01-B - All Controllers Xml'))
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')
        # print(PrettyFormatAny.form(self.m_xml.controller, 'A3-01-C - First Controller Xml'))

    def test_02_ExtractXML(self):
        l_controllers = self.m_ctlr_api.read_all_controllers_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_controllers[0], 'A3-02-a - First Controller Obj'))
        l_interface = interfaceXml.read_interface_xml(self.m_controller_obj, l_controllers[0])


class R1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)

    def test_01_All(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_controllers = self.m_ctlr_api.read_all_controllers_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Lighting.Controllers = l_controllers
        print(PrettyFormatAny.form(l_controllers[0], 'R1-01-A - Controller Obj'))
        print(PrettyFormatAny.form(self.m_xml.controller, 'R1-01-B - Controller Xml'))
        interfaceXml.read_interface_xml(l_controllers[0], self.m_xml.controller)
        print(PrettyFormatAny.form(l_controllers[0], 'R1-01-C - Controller Obj'))


class W1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """

    def test_02_ExtractXML(self):
        l_controllers = self.m_ctlr_api.read_all_controllers_xml(self.m_pyhouse_obj)
        l_interface = interfaceXml.read_interface_xml(self.m_controller_obj, l_controllers[0])

# ## END
