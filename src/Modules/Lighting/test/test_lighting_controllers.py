"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb 21, 2014
@summary:   This module is for testing local node data.

Passed all 10 tests - DBK - 2014-07-18
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Lighting.lighting_controllers import LCApi
from Modules.Lighting.test.xml_core import TESTING_LIGHTING_CORE_COMMENT, TESTING_LIGHTING_CORE_ROOM
from Modules.Families.family import API as familyAPI
from Modules.Families.Insteon.test.xml_insteon import TESTING_INSTEON_ADDRESS
from Modules.Core import conversions
from Modules.Web import web_utils
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = self.m_family
        self.m_api = LCApi(self.m_pyhouse_obj)
        self.m_controller_obj = ControllerData()



class A1(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_02_Xml(self):
        PrettyPrintAny(self.m_xml.controller, 'Controller')

    def test_03_Family(self):
        PrettyPrintAny(self.m_family, 'Family')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Base Data')
        self.assertEqual(l_obj.Name, 'Insteon Serial Controller')
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.LightingType, 'Controller')
        self.assertEqual(l_obj.Comment, TESTING_LIGHTING_CORE_COMMENT)
        self.assertEqual(l_obj.RoomName, TESTING_LIGHTING_CORE_ROOM)

    def test_02_Controller(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        l_obj = self.m_api._read_controller_data(l_obj, self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Base+Controller Data')
        self.assertEqual(l_obj.InterfaceType, 'Serial')
        self.assertEqual(l_obj.Port, '/dev/ttyS0')

    def test_03_Interface(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        self.m_api._read_controller_data(l_obj, self.m_xml.controller)
        self.m_api._read_interface_data(l_obj, self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Base+Controller+Interface')
        self.assertEqual(l_obj.BaudRate, 19200)
        self.assertEqual(l_obj.ByteSize, 8)
        self.assertEqual(l_obj.Parity, 'N')
        self.assertEqual(l_obj.RtsCts, False)
        self.assertEqual(l_obj.StopBits, 1.0)
        self.assertEqual(l_obj.Timeout, 1.0)
        self.assertEqual(l_obj.XonXoff, False)

    def test_04_Family(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        self.m_api._read_controller_data(l_obj, self.m_xml.controller)
        self.m_api._read_interface_data(l_obj, self.m_xml.controller)
        self.m_api._read_family_data(l_obj, self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Read Family', 100)
        self.assertEqual(l_obj.DevCat, conversions.dotted_hex2int('02.1C'))
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))

    def test_06_OneController(self):
        """ Read in the xml file and fill in the lights
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_xml.controller)
        PrettyPrintAny(l_controller, 'OneController', 100)
        self.assertEqual(l_controller.BaudRate, 19200)
        self.assertEqual(l_controller.ByteSize, 8, 'Bad Byte Size')
        self.assertEqual(l_controller.DsrDtr, False, 'Bad DsrDtr')
        self.assertEqual(l_controller.DeviceFamily, 'Insteon')
        self.assertEqual(l_controller.InterfaceType, 'Serial')
        self.assertEqual(l_controller.Parity, 'N')
        self.assertEqual(l_controller.RtsCts, False)
        self.assertEqual(l_controller.StopBits, 1.0)
        self.assertEqual(l_controller.LightingType, 'Controller')
        self.assertEqual(l_controller.XonXoff, False)
        self.assertEqual(l_controller.DeviceFamily, 'Insteon')
        self.assertEqual(l_controller.LightingType, 'Controller')

    def test_07_AllControllers(self):
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        self.assertEqual(len(l_controllers), 2)
        PrettyPrintAny(l_controllers, 'AllControllers')


class C1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base(self):
        """ Write out the XML file for the Base controller
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        l_xml = self.m_api._write_base_data(l_controllers[0])
        PrettyPrintAny(l_xml, 'Base')

    def test_02_Controller(self):
        """ Write out the XML file for the Base + Controller
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        l_xml = self.m_api._write_base_data(l_controllers[0])
        self.m_api._write_controller_data(l_controllers[0], l_xml)
        PrettyPrintAny(l_xml, 'Controller')

    def test_03_Interface(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        l_xml = self.m_api._write_base_data(l_controllers[0])
        self.m_api._write_controller_data(l_controllers[0], l_xml)
        self.m_api._write_interface_data(l_controllers[0], l_xml)
        PrettyPrintAny(l_xml, 'Controller')

    def test_04_Family(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        l_xml = self.m_api._write_base_data(l_controllers[0])
        self.m_api._write_controller_data(l_controllers[0], l_xml)
        self.m_api._write_interface_data(l_controllers[0], l_xml)
        self.m_api._write_family_data(l_controllers[0], l_xml)
        PrettyPrintAny(l_xml, 'Controller')

    def test_04_OneXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        l_xml = self.m_api.write_one_controller_xml(l_controllers[0])
        PrettyPrintAny(l_xml, 'OneController')

    def test_05_AllXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        l_xml = self.m_api.write_all_controllers_xml(l_controllers)
        PrettyPrintAny(l_xml, 'AllControllers', 100)



class C2_JSON(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_controller = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_controller))
        PrettyPrintAny(l_json, 'JSON', 100)


def suite():
    suite = unittest.TestSuite()
    # suite.addTests(Test_02_XML())
    return suite

# ## END DBK
