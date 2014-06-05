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
from Modules.Core.data_objects import PyHouseData, HouseData
from Modules.lights import lighting_controllers
from Modules.web import web_utils
from Modules.utils.xml_tools import PrettifyXML
from src.test import xml_data
from src.Modules.utils.tools import PrettyPrintAny

XML = xml_data.XML_LONG


class Test_02_XML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses_xml = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_controllers_xml = self.m_house_xml.find('Controllers')
        self.m_controller_xml = self.m_controllers_xml.find('Controller')
        self.m_api = lighting_controllers.ControllersAPI()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_controllers_xml.tag, 'Controllers', 'XML - No Controllers section')
        self.assertEqual(self.m_controller_xml.tag, 'Controller', 'XML - No Controller section')

    def test_0203_ReadOneControllerXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_controller_xml)
        PrettyPrintAny(l_controller)
        self.assertEqual(l_controller.Active, False, 'Bad Active')
        self.assertEqual(l_controller.BaudRate, 19200, 'Bad BaudRate')
        self.assertEqual(l_controller.ByteSize, 8, 'Bad Byte Size')
        self.assertEqual(l_controller.Comment, 'Dongle using serial converter 067B:2303', 'Bad Comments')
        self.assertEqual(l_controller.Coords, 'None', 'Bad Coords')
        self.assertEqual(l_controller.Dimmable, True, 'Bad Dimmable')
        self.assertEqual(l_controller.DsrDtr, False, 'Bad DsrDtr')
        self.assertEqual(l_controller.Family, 'Insteon', 'Bad Family')
        self.assertEqual(l_controller.Interface, 'Serial', 'Bad Interface')
        self.assertEqual(l_controller.Key, 0, 'Bad Key')
        self.assertEqual(l_controller.Name, 'PLM_1', 'Bad Name')
        self.assertEqual(l_controller.Parity, 'N', 'Bad Parity')
        self.assertEqual(l_controller.RoomName, 'Office', 'Bad Room Name')
        self.assertEqual(l_controller.RtsCts, False, 'Bad RtsCts')
        self.assertEqual(l_controller.StopBits, 1.0, 'Bad Stop Bits')
        self.assertEqual(l_controller.Type, 'Controller', 'Bad Type')
        self.assertEqual(l_controller.XonXoff, False, 'Bad XonXoff')

    def test_0204_ReadControllersXml(self):
        l_controllers = self.m_api.read_controllers_xml(self.m_house_xml)
        print('Controllers {0:}'.format(l_controllers))
        self.assertEqual(len(l_controllers), 3)

    def test_0211_WriteOneControllerXml(self):
        """ Write out the XML file for the location section
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_controller_xml)
        l_xml = self.m_api.write_one_controller_xml(l_controller)
        print('XML: {0:}'.format(PrettifyXML(l_xml)))

    def test_0212_WriteControllersXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_controllers_xml(self.m_house_xml)
        l_xml = self.m_api.write_controllers_xml(l_controllers)
        print('XML: {0:}'.format(PrettifyXML(l_xml)))

    def test_0221_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_controller = self.m_api.read_controllers_xml(self.m_house_xml)
        print('ControllerS: {0:}'.format(l_controller))
        print('Controller 0: {0:}'.format(vars(l_controller[0])))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_controller))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
