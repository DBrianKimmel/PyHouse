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
        PrettyPrintAny(self, 'TestLighting - ', 80)

        self.m_house_xml = self.m_root_xml.find('HouseDivision')
        self.m_controllers_xml = self.m_house_xml.find('ControllerSection')
        self.m_controller_xml = self.m_controllers_xml.find('Controller')
        print('test_schedule.SetupMixin')


class Test_02_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)
        self.m_pyhouse_obj.HouseObjs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = lighting_controllers.ControllersAPI(self.m_pyhouse_obj)

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_controllers_xml.tag, 'Controllers', 'XML - No Controllers section')
        self.assertEqual(self.m_controller_xml.tag, 'Controller', 'XML - No Controller section')

    def test_0221_ReadInterfaceXml(self):
        pass

    def test_0222_ReadFamilyXml(self):
        pass

    def test_0223_ReadControllerXml(self):
        pass

    def test_0243_ReadOneControllerXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_controller_xml)
        PrettyPrintAny(l_controller)
        self.assertEqual(l_controller.Active, False, 'Bad Active')
        self.assertEqual(l_controller.BaudRate, 19200, 'Bad BaudRate')
        self.assertEqual(l_controller.ByteSize, 8, 'Bad Byte Size')
        self.assertEqual(l_controller.Comment, 'Dongle using serial converter 067B:2303', 'Bad Comments')
        self.assertEqual(l_controller.Coords, 'None', 'Bad Coords')
        self.assertEqual(l_controller.IsDimmable, True, 'Bad Dimmable')
        self.assertEqual(l_controller.DsrDtr, False, 'Bad DsrDtr')
        self.assertEqual(l_controller.LightingFamily, 'Insteon', 'Bad LightingFamily')
        self.assertEqual(l_controller.InterfaceType, 'Serial', 'Bad InterfaceType')
        self.assertEqual(l_controller.Key, 0, 'Bad Key')
        self.assertEqual(l_controller.Name, 'PLM_1', 'Bad Name')
        self.assertEqual(l_controller.Parity, 'N', 'Bad Parity')
        self.assertEqual(l_controller.RoomName, 'Office', 'Bad Room Name')
        self.assertEqual(l_controller.RtsCts, False, 'Bad RtsCts')
        self.assertEqual(l_controller.StopBits, 1.0, 'Bad Stop Bits')
        self.assertEqual(l_controller.LightingType, 'Controller', 'Bad LightingType')
        self.assertEqual(l_controller.XonXoff, False, 'Bad XonXoff')

    def test_0244_ReadControllersXml(self):
        l_controllers = self.m_api.read_controllers_xml(self.m_pyhouse_obj)
        print('Controllers {0:}'.format(l_controllers))
        self.assertEqual(len(l_controllers), 3)

    def test_0261_WriteOneControllerXml(self):
        """ Write out the XML file for the location section
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_controller_xml)
        l_xml = self.m_api.write_one_controller_xml(l_controller)
        print('XML: {0:}'.format(PrettyPrintAny(l_xml)))

    def test_0262_WriteControllersXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_controllers_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_controllers_xml(l_controllers)
        print('XML: {0:}'.format(PrettyPrintAny(l_xml)))

    def test_0281_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_controller = self.m_api.read_controllers_xml(self.m_pyhouse_obj)
        print('ControllerS: {0:}'.format(l_controller))
        print('Controller 0: {0:}'.format(vars(l_controller[0])))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_controller))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
