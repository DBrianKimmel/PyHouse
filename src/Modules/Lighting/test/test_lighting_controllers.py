"""
@name: PyHouse/src/Modules/Lighting/test/test_lighting_controllers.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Feb 21, 2014
@summary: This module is for testing local node data.

Passed all 10 tests - DBK - 2014-07-18
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Lighting import lighting_controllers
from Modules.Families import family
from Modules.Core import conversions
from Modules.Web import web_utils
from test.xml_data import *
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = lighting_controllers.ControllersAPI(self.m_pyhouse_obj)
        self.m_controller_obj = ControllerData()



class C01_XML(SetupMixin, unittest.TestCase):
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



class C02_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseData(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Base Data')
        self.assertEqual(l_obj.Name, 'Insteon Serial Controller')
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.LightingType, 'Controller')
        self.assertEqual(l_obj.Comment, TESTING_LIGHTING_CORE_COMMENT)
        self.assertEqual(l_obj.Coords, TESTING_LIGHTING_CORE_COORDS)
        self.assertEqual(l_obj.RoomName, TESTING_LIGHTING_CORE_ROOM)
        self.assertEqual(l_obj.IsDimmable, TESTING_LIGHTING_CORE_DIMMABLE)

    def test_02_ControllerData(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        l_obj = self.m_api._read_controller_data(l_obj, self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Base+Controller Data')
        self.assertEqual(l_obj.InterfaceType, 'Serial')
        self.assertEqual(l_obj.Port, '/dev/ttyS0')

    def test_03_InterfaceXml(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        l_obj = self.m_api._read_controller_data(l_obj, self.m_xml.controller)
        l_interface = self.m_api._read_interface_data(l_obj, self.m_xml.controller)
        PrettyPrintAny(l_interface, 'Base+Controller+Interface')
        self.assertEqual(l_obj.BaudRate, 19200)
        self.assertEqual(l_obj.ByteSize, 8)
        self.assertEqual(l_obj.Parity, 'N')
        self.assertEqual(l_obj.RtsCts, False)
        self.assertEqual(l_obj.StopBits, 1.0)
        self.assertEqual(l_obj.Timeout, 1.0)
        self.assertEqual(l_obj.XonXoff, False)

    def test_05_Family(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        l_obj = self.m_api._read_controller_data(l_obj, self.m_xml.controller)
        _l_family = self.m_api._read_family_data(l_obj, self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Read Family', 100)
        self.assertEqual(l_obj.DevCat, conversions.dotted_hex2int('02.1C'))
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))

    def test_06_OneController(self):
        """ Read in the xml file and fill in the lights
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_xml.controller)
        self.assertEqual(l_controller.BaudRate, 19200, 'Bad BaudRate')
        self.assertEqual(l_controller.ByteSize, 8, 'Bad Byte Size')
        self.assertEqual(l_controller.DsrDtr, False, 'Bad DsrDtr')
        self.assertEqual(l_controller.ControllerFamily, 'Insteon', 'Bad ControllerFamily')
        self.assertEqual(l_controller.InterfaceType, 'Serial', 'Bad InterfaceType')
        self.assertEqual(l_controller.Parity, 'N', 'Bad Parity')
        self.assertEqual(l_controller.RtsCts, False, 'Bad RtsCts')
        self.assertEqual(l_controller.StopBits, 1.0, 'Bad Stop Bits')
        self.assertEqual(l_controller.LightingType, 'Controller', 'Bad LightingType')
        self.assertEqual(l_controller.XonXoff, False, 'Bad XonXoff')
        self.assertEqual(l_controller.ControllerFamily, 'Insteon', 'Bad Lighting family')
        self.assertEqual(l_controller.LightingType, 'Controller', 'Bad LightingType')
        PrettyPrintAny(l_controller, 'OneController', 100)

    def test_07_AllControllers(self):
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        self.assertEqual(len(l_controllers), 2)
        PrettyPrintAny(l_controllers, 'AllControllers', 100)

class C03_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneControllerXml(self):
        """ Write out the XML file for the location section
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_xml.controller)
        l_xml = self.m_api.write_one_controller_xml(l_controller)
        PrettyPrintAny(l_xml, 'OneController')

    def test_02_ControllersXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_xml.controller_sect)
        l_xml = self.m_api.write_controllers_xml(l_controllers)
        PrettyPrintAny(l_xml, 'AllControllers', 100)



class C04_JSON(SetupMixin, unittest.TestCase):
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
