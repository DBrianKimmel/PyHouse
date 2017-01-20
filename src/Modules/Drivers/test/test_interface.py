"""
@name:      PyHouse/src/Modules/Drivers/test/test_interface.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   This module is for testing driver interface data.

Passed all 6 tests - DBK - 2016-11-22
"""

__updated__ = '2017-01-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import ControllerData
from Modules.Drivers.interface import Xml as interfaceXml
from Modules.Housing.Lighting.lighting_controllers import API as controllerAPI

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
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_02_ExtractXML(self):
        l_controllers = self.m_ctlr_api.read_all_controllers_xml(self.m_pyhouse_obj)
        l_interface = interfaceXml.read_interface_xml(self.m_controller_obj, l_controllers[0])


class C2_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)

    def test_02_All(self):
        """ Be sure that the XML contains the right stuff.
        """
        interfaceXml.read_interface_xml(self.m_controller_obj, self.m_xml.controller)


class C03_Write(SetupMixin, unittest.TestCase):
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
