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
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = lighting_controllers.ControllersAPI(self.m_pyhouse_obj)
        self.m_controller_obj = ControllerData()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_0210_BaseData(self):
        l_obj = self.m_api._read_base_data(self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Base Data')
        self.assertEqual(l_obj.Name, 'PLM_1')
        self.assertEqual(l_obj.Active, False)
        self.assertEqual(l_obj.LightingType, 'Controller')

    def test_0211_ReadControllerData(self):
        l_obj = self.m_api._read_controller_data(self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Controller Data')
        self.assertEqual(l_obj.InterfaceType, 'Serial')
        self.assertEqual(l_obj.Port, '/dev/ttyUSB0')

    def test_0221_ReadInterfaceXml(self):
        l_obj = self.m_api._read_controller_data(self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Read Interface A')
        l_interface = self.m_api._read_interface_data(l_obj, self.m_xml.controller)
        PrettyPrintAny(l_interface, 'Read Interface B')
        self.assertEqual(l_obj.BaudRate, 19200)
        self.assertEqual(l_obj.ByteSize, 8)
        self.assertEqual(l_obj.Parity, 'N')
        self.assertEqual(l_obj.RtsCts, False)
        self.assertEqual(l_obj.StopBits, 1.0)
        self.assertEqual(l_obj.Timeout, 1.0)
        self.assertEqual(l_obj.XonXoff, False)

    def test_0222_ReadFamilyXml(self):
        l_obj = self.m_api._read_controller_data(self.m_xml.controller)
        l_family = self.m_api._read_family_data(l_obj, self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Read Family', 100)
        self.assertEqual(l_obj.DevCat, conversions.dotted_hex2int('12.34'))
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int('AA.AA.AA'))

    def test_0223_ReadControllerXml(self):
        l_controller = self.m_api._read_controller_data(self.m_xml.controller)
        PrettyPrintAny(l_controller, 'Read Controller', 100)

    def test_0243_ReadOneControllerXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_xml.controller)
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
        self.assertEqual(l_controller.ControllerFamily, 'Insteon', 'Bad Lighting family')
        self.assertEqual(l_controller.LightingType, 'Controller', 'Bad LightingType')
        self.assertEqual(l_controller.InsteonAddress, conversions.dotted_hex2int('AA.AA.AA'))
        PrettyPrintAny(l_controller, 'OneController', 100)

    def test_0244_ReadAllControllersXml(self):
        l_controllers = self.m_api.read_controllers_xml(self.m_xml.controller_sect)
        self.assertEqual(len(l_controllers), 3)
        PrettyPrintAny(l_controllers, 'AllControllers', 100)

    def test_0261_WriteOneControllerXml(self):
        """ Write out the XML file for the location section
        """
        l_controller = self.m_api.read_one_controller_xml(self.m_xml.controller)
        l_xml = self.m_api.write_one_controller_xml(l_controller)
        PrettyPrintAny(l_xml, 'OneController')

    def test_0262_WriteControllersXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_controllers_xml(self.m_xml.controller_sect)
        l_xml = self.m_api.write_controllers_xml(l_controllers)
        PrettyPrintAny(l_xml, 'AllControllers', 100)

    def test_0281_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_controller = self.m_api.read_controllers_xml(self.m_xml.controller_sect)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_controller))
        PrettyPrintAny(l_json, 'JSON', 100)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(Test_02_XML())
    return suite

# ## END DBK
