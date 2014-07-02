"""
@name: PyHouse/src/Modules/lights/test/test_lighting_controllers.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Feb 21, 2014
@summary: This module is for testing local node data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, ControllerData
from Modules.lights import lighting_controllers
from Modules.families import family
from Modules.web import web_utils
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data, test_mixin


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup().BuildPyHouse()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_controller_sect_xml = self.m_house_div_xml.find('ControllerSection')
        self.m_controller_xml = self.m_controller_sect_xml.find('Controller')
        self.m_controller_obj = ControllerData()

        self.m_api = lighting_controllers.ControllersAPI(self.m_pyhouse_obj)

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_controller_sect_xml.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_controller_xml.tag, 'Controller', 'XML - No Controller section')

    def test_0221_ReadInterfaceXml(self):
        l_interface = self.m_api._read_interface_data(self.m_controller_obj, self.m_controller_xml)
        PrettyPrintAny(l_interface, 'Read Interface', 100)

    def test_0222_ReadFamilyXml(self):
        self.m_controller_obj.ControllerFamily = 'Insteon'
        l_family = self.m_api._read_family_data(self.m_controller_obj, self.m_controller_xml)
        PrettyPrintAny(l_family, 'Read Family', 100)

    def test_0223_ReadControllerXml(self):
        l_controller = self.m_api._read_controller_data(self.m_controller_obj, self.m_controller_xml)
        PrettyPrintAny(l_controller, 'Read Controller', 100)

    def test_0243_ReadOneControllerXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_controller_xml)
        self.assertEqual(l_controller.Active, False, 'Bad Active')
        self.assertEqual(l_controller.BaudRate, 19200, 'Bad BaudRate')
        self.assertEqual(l_controller.ByteSize, 8, 'Bad Byte Size')
        self.assertEqual(l_controller.Comment, 'Dongle using serial converter 067B:2303', 'Bad Comments')
        self.assertEqual(l_controller.Coords, 'None', 'Bad Coords')
        self.assertEqual(l_controller.IsDimmable, False, 'Bad Dimmable')
        self.assertEqual(l_controller.DsrDtr, False, 'Bad DsrDtr')
        self.assertEqual(l_controller.ControllerFamily, 'Insteon', 'Bad ControllerFamily')
        self.assertEqual(l_controller.InterfaceType, 'Serial', 'Bad InterfaceType')
        self.assertEqual(l_controller.Key, 0, 'Bad Key')
        self.assertEqual(l_controller.Name, 'PLM_1', 'Bad Name')
        self.assertEqual(l_controller.Parity, 'N', 'Bad Parity')
        self.assertEqual(l_controller.RoomName, 'Office', 'Bad Room Name')
        self.assertEqual(l_controller.RtsCts, False, 'Bad RtsCts')
        self.assertEqual(l_controller.StopBits, 1.0, 'Bad Stop Bits')
        self.assertEqual(l_controller.LightingType, 'Controller', 'Bad LightingType')
        self.assertEqual(l_controller.XonXoff, False, 'Bad XonXoff')
        PrettyPrintAny(l_controller, 'OneController', 100)

    def test_0244_ReadAllControllersXml(self):
        l_controllers = self.m_api.read_controllers_xml(self.m_controller_sect_xml)
        self.assertEqual(len(l_controllers), 3)
        PrettyPrintAny(l_controllers, 'AllControllers', 100)

    def test_0261_WriteOneControllerXml(self):
        """ Write out the XML file for the location section
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_controller_xml)
        l_xml = self.m_api.write_one_controller_xml(l_controller)
        PrettyPrintAny(l_xml, 'OneController')

    def test_0262_WriteControllersXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_controllers_xml(self.m_controller_sect_xml)
        l_xml = self.m_api.write_controllers_xml(l_controllers)
        PrettyPrintAny(l_xml, 'AllControllers', 100)

    def test_0281_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_controller = self.m_api.read_controllers_xml(self.m_controller_sect_xml)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_controller))
        PrettyPrintAny(l_json, 'JSON', 100)


class Test_03_GetExternalIp(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_api = lighting_controllers.ControllersAPI(None)

    def test_0301_createClient(self):
        # l_client = self.m_api.Start(self.m_pyhouse_obj, self.m_house_obj, self.m_house_xml)
        pass

# ## END DBK
