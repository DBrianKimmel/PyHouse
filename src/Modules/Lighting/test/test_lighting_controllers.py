"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb 21, 2014
@summary:   This module is for testing local node data.

Passed all 19 tests - DBK - 2015-08-02
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Core.test.xml_device import TESTING_DEVICE_COMMENT, TESTING_DEVICE_FAMILY, TESTING_DEVICE_TYPE, TESTING_DEVICE_SUBTYPE, \
    TESTING_DEVICE_ROOM_NAME
from Modules.Lighting.lighting_controllers import Utility, API as controllerAPI
from Modules.Lighting.test.xml_core import TESTING_LIGHTING_CORE_ROOM
from Modules.Families.family import API as familyAPI
from Modules.Families.Insteon.test.xml_insteon import \
        TESTING_INSTEON_ADDRESS, \
        TESTING_INSTEON_DEVCAT, \
        TESTING_INSTEON_GROUP_LIST, \
        TESTING_INSTEON_GROUP_NUM, \
        TESTING_INSTEON_MASTER, \
        TESTING_INSTEON_PRODUCT_KEY

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
        self.m_pyhouse_obj.House.FamilyData = self.m_family
        self.m_api = controllerAPI()
        self.m_controller_obj = ControllerData()
        self.m_version = '1.4.0'



class A1(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')

    def test_02_Xml(self):
        # PrettyPrintAny(self.m_xml.controller, 'Controller')
        pass

    def test_03_Family(self):
        # PrettyPrintAny(self.m_family, 'Family')
        # PrettyPrintAny(self.m_family['Insteon'], 'Insteon Family')
        self.assertEqual(self.m_family['Insteon'].Name, 'Insteon')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseDevice(self):
        l_obj = Utility._read_base_device(self.m_xml.controller, self.m_version)
        # PrettyPrintAny(l_obj, 'Base Data')
        self.assertEqual(l_obj.Name, 'Insteon Serial Controller')
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.LightingType, 'Controller')
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_obj.DeviceType, int(TESTING_DEVICE_TYPE))
        self.assertEqual(l_obj.DeviceSubType, int(TESTING_DEVICE_SUBTYPE))
        self.assertEqual(l_obj.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_02_Controller(self):
        l_obj = Utility._read_base_device(self.m_xml.controller, self.m_version)
        l_obj = Utility._read_controller_data(l_obj, self.m_xml.controller, self.m_version)
        # PrettyPrintAny(l_obj, 'Base+Controller Data')
        self.assertEqual(l_obj.InterfaceType, 'Serial')
        self.assertEqual(l_obj.Port, '/dev/ttyS0')

    def test_03_Interface(self):
        l_obj = Utility._read_base_device(self.m_xml.controller, self.m_version)
        Utility._read_controller_data(l_obj, self.m_xml.controller, self.m_version)
        Utility._read_interface_data(l_obj, self.m_xml.controller, self.m_version)
        # PrettyPrintAny(l_obj, 'Base+Controller+Interface')
        self.assertEqual(l_obj.BaudRate, 19200)
        self.assertEqual(l_obj.ByteSize, 8)
        self.assertEqual(l_obj.Parity, 'N')
        self.assertEqual(l_obj.RtsCts, False)
        self.assertEqual(l_obj.StopBits, 1.0)
        self.assertEqual(l_obj.Timeout, 1.0)
        self.assertEqual(l_obj.XonXoff, False)

    def test_04_Family(self):
        l_obj = Utility._read_base_device(self.m_xml.controller, self.m_version)
        Utility._read_controller_data(l_obj, self.m_xml.controller, self.m_version)
        Utility._read_interface_data(l_obj, self.m_xml.controller, self.m_version)
        Utility._read_family_data(self.m_pyhouse_obj, l_obj, self.m_xml.controller, self.m_version)
        # PrettyPrintAny(l_obj, 'Read Family', 100)
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))
        self.assertEqual(l_obj.DevCat, conversions.dotted_hex2int(TESTING_INSTEON_DEVCAT))
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_obj.GroupNumber, int(TESTING_INSTEON_GROUP_NUM))
        self.assertEqual(l_obj.IsMaster, bool(TESTING_INSTEON_MASTER))

    def test_06_OneController(self):
        """ Read in the xml file and fill in the lights
        """
        l_controller = Utility._read_one_controller_xml(self.m_pyhouse_obj, self.m_xml.controller, self.m_version)
        # PrettyPrintAny(l_controller, 'OneController', 100)
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
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        # PrettyPrintAny(l_controllers, 'AllControllers')
        self.assertEqual(len(l_controllers), 2)


class C1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base(self):
        """ Write out the XML file for the Base controller
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_xml = Utility._write_base_device(l_controllers[0])
        # PrettyPrintAny(l_xml, 'Base')

    def test_02_Controller(self):
        """ Write out the XML file for the Base + Controller
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_xml = Utility._write_base_device(l_controllers[0])
        Utility._write_controller_data(l_controllers[0], l_xml)
        # PrettyPrintAny(l_xml, 'Controller')

    def test_03_Interface(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_xml = Utility._write_base_device(l_controllers[0])
        Utility._write_controller_data(l_controllers[0], l_xml)
        Utility._write_interface_data(l_controllers[0], l_xml)
        # PrettyPrintAny(l_xml, 'Controller')

    def test_04_Family(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_xml = Utility._write_base_device(l_controllers[0])
        Utility._write_controller_data(l_controllers[0], l_xml)
        Utility._write_interface_data(l_controllers[0], l_xml)
        Utility._write_family_data(self.m_pyhouse_obj, l_controllers[0], l_xml)
        # PrettyPrintAny(l_xml, 'Controller')

    def test_04_OneXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_xml = Utility._write_one_controller_xml(self.m_pyhouse_obj, l_controllers[0])
        # PrettyPrintAny(l_xml, 'OneController')

    def test_05_AllXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        self.m_pyhouse_obj.House.Controllers = l_controllers
        l_xml = self.m_api.write_all_controllers_xml(self.m_pyhouse_obj)
        # PrettyPrintAny(l_xml, 'AllControllers', 100)



class C2_JSON(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_controller = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_controller))
        # PrettyPrintAny(l_json, 'JSON', 100)


def suite():
    suite = unittest.TestSuite()
    # suite.addTests(Test_02_XML())
    return suite

# ## END DBK
