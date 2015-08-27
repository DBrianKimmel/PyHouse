"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb 21, 2014
@summary:   This module is for testing local node data.

Passed all 16 tests - DBK - 2015-08-17
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Lighting.lighting_controllers import Utility, API as controllerAPI
from Modules.Families.family import API as familyAPI
from Modules.Core import conversions
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.test.xml_device import \
        TESTING_DEVICE_COMMENT, \
        TESTING_DEVICE_FAMILY_INSTEON, \
        TESTING_DEVICE_TYPE, \
        TESTING_DEVICE_SUBTYPE, \
        TESTING_DEVICE_ROOM_NAME
from Modules.Drivers.Serial.test.xml_serial import \
        TESTING_SERIAL_BAUD_RATE, \
        TESTING_SERIAL_BYTE_SIZE, \
        TESTING_SERIAL_DSR_DTR, TESTING_SERIAL_PARITY, TESTING_SERIAL_RTS_CTS, TESTING_SERIAL_STOP_BITS, TESTING_SERIAL_TIMEOUT, \
    TESTING_SERIAL_XON_XOFF
from Modules.Drivers.USB.test.xml_usb import \
        TESTING_USB_VENDOR, \
        TESTING_USB_PRODUCT
from Modules.Drivers.test.xml_interface import \
        TESTING_INTERFACE_TYPE_SERIAL, \
        TESTING_INTERFACE_PORT_SERIAL
from Modules.Lighting.test.xml_controllers import \
        TESTING_CONTROLLER_NAME_0, \
        TESTING_CONTROLLER_ACTIVE_0, \
        TESTING_CONTROLLER_TYPE, \
        TESTING_CONTROLLER_KEY_0
from Modules.Families.Insteon.test.xml_insteon import \
        TESTING_INSTEON_ADDRESS, \
        TESTING_INSTEON_DEVCAT, \
        TESTING_INSTEON_GROUP_LIST, \
        TESTING_INSTEON_GROUP_NUM, \
        TESTING_INSTEON_VERSION, \
        TESTING_INSTEON_PRODUCT_KEY
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Utilities import json_tools


class SetupMixin(object):

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
        """Read Base Device
        """
        l_obj = Utility._read_base_device(self.m_xml.controller, self.m_version)
        self.assertEqual(l_obj.Name, TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_obj.Active, (TESTING_CONTROLLER_ACTIVE_0 == 'True'))
        self.assertEqual(l_obj.LightingType, TESTING_CONTROLLER_TYPE)
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_obj.DeviceType, int(TESTING_DEVICE_TYPE))
        self.assertEqual(l_obj.DeviceSubType, int(TESTING_DEVICE_SUBTYPE))
        self.assertEqual(l_obj.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_02_Controller(self):
        """Read Controller 0 Serial
        """
        l_obj = Utility._read_base_device(self.m_xml.controller, self.m_version)
        l_obj = Utility._read_controller_data(l_obj, self.m_xml.controller, self.m_version)
        self.assertEqual(l_obj.InterfaceType, TESTING_INTERFACE_TYPE_SERIAL)
        self.assertEqual(l_obj.Port, TESTING_INTERFACE_PORT_SERIAL)

    def test_03_Interface(self):
        """Read Controller Interface.
        """
        l_obj = Utility._read_base_device(self.m_xml.controller, self.m_version)
        Utility._read_controller_data(l_obj, self.m_xml.controller, self.m_version)
        Utility._read_interface_data(l_obj, self.m_xml.controller, self.m_version)
        # PrettyPrintAny(l_obj, 'Base+Controller+Interface')
        self.assertEqual(l_obj.BaudRate, int(TESTING_SERIAL_BAUD_RATE))
        self.assertEqual(l_obj.ByteSize, int(TESTING_SERIAL_BYTE_SIZE))
        self.assertEqual(l_obj.Parity, TESTING_SERIAL_PARITY)
        self.assertEqual(l_obj.RtsCts, TESTING_SERIAL_RTS_CTS == 'True')
        self.assertEqual(l_obj.StopBits, float(TESTING_SERIAL_STOP_BITS))
        self.assertEqual(l_obj.Timeout, float(TESTING_SERIAL_TIMEOUT))
        self.assertEqual(l_obj.XonXoff, TESTING_SERIAL_XON_XOFF == 'True')

    def test_04_Family(self):
        """Read controller family
        """
        l_obj = Utility._read_base_device(self.m_xml.controller, self.m_version)
        Utility._read_controller_data(l_obj, self.m_xml.controller, self.m_version)
        Utility._read_interface_data(l_obj, self.m_xml.controller, self.m_version)
        Utility._read_family_data(self.m_pyhouse_obj, l_obj, self.m_xml.controller, self.m_version)
        # PrettyPrintAny(l_obj, 'Read Family', 100)
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))
        self.assertEqual(l_obj.DevCat, conversions.dotted_hex2int(TESTING_INSTEON_DEVCAT))
        self.assertEqual(l_obj.ProductKey, conversions.dotted_hex2int(TESTING_INSTEON_PRODUCT_KEY))
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_obj.GroupNumber, int(TESTING_INSTEON_GROUP_NUM))
        self.assertEqual(l_obj.Version, int(TESTING_INSTEON_VERSION))

    def test_06_OneController(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = Utility._read_one_controller_xml(self.m_pyhouse_obj, self.m_xml.controller, self.m_version)
        print(PrettyFormatAny.form(l_obj, 'OneController', 100))
        self.assertEqual(l_obj.Name, TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_obj.Active, (TESTING_CONTROLLER_ACTIVE_0 == 'True'))
        self.assertEqual(l_obj.LightingType, TESTING_CONTROLLER_TYPE)
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_obj.DeviceType, int(TESTING_DEVICE_TYPE))
        self.assertEqual(l_obj.DeviceSubType, int(TESTING_DEVICE_SUBTYPE))
        self.assertEqual(l_obj.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_obj.InterfaceType, TESTING_INTERFACE_TYPE_SERIAL)
        self.assertEqual(l_obj.Port, TESTING_INTERFACE_PORT_SERIAL)
        self.assertEqual(l_obj.BaudRate, int(TESTING_SERIAL_BAUD_RATE))
        self.assertEqual(l_obj.ByteSize, int(TESTING_SERIAL_BYTE_SIZE))
        self.assertEqual(l_obj.Parity, TESTING_SERIAL_PARITY)
        self.assertEqual(l_obj.RtsCts, TESTING_SERIAL_RTS_CTS == 'True')
        self.assertEqual(l_obj.StopBits, float(TESTING_SERIAL_STOP_BITS))
        self.assertEqual(l_obj.Timeout, float(TESTING_SERIAL_TIMEOUT))
        self.assertEqual(l_obj.XonXoff, TESTING_SERIAL_XON_XOFF == 'True')
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))
        self.assertEqual(l_obj.DevCat, conversions.dotted_hex2int(TESTING_INSTEON_DEVCAT))
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_obj.GroupNumber, int(TESTING_INSTEON_GROUP_NUM))

    def test_07_AllControllers(self):
        """Read all controllers.
        """
        l_objs = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        # print(PrettyFormatAny.form(l_objs[1], 'AllControllers'))
        self.assertEqual(len(l_objs), 2)
        self.assertEqual(l_objs[0].BaudRate, int(TESTING_SERIAL_BAUD_RATE))
        self.assertEqual(l_objs[0].ByteSize, int(TESTING_SERIAL_BYTE_SIZE))
        self.assertEqual(l_objs[0].DsrDtr, (TESTING_SERIAL_DSR_DTR == 'True'))
        self.assertEqual(l_objs[1].Vendor, int(TESTING_USB_VENDOR))
        self.assertEqual(l_objs[1].Product, int(TESTING_USB_PRODUCT))


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
        # print(PrettyFormatAny.form(l_xml, 'Base'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_CONTROLLER_KEY_0)
        self.assertEqual(bool(l_xml.attrib['Active']), TESTING_CONTROLLER_ACTIVE_0 == 'True')
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_DEVICE_TYPE)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_DEVICE_SUBTYPE)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_DEVICE_ROOM_NAME)

    def test_02_Controller(self):
        """ Write out the XML file for the Base + Controller
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_xml = Utility._write_base_device(l_controllers[0])
        Utility._write_controller_data(l_controllers[0], l_xml)
        self.assertEqual(l_xml.find('InterfaceType').text, TESTING_INTERFACE_TYPE_SERIAL)
        self.assertEqual(l_xml.find('Port').text, TESTING_INTERFACE_PORT_SERIAL)

    def test_03_Interface(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        # print(PrettyFormatAny.form(l_controllers[0], 'Obj Controllers', 100))
        l_xml = Utility._write_base_device(l_controllers[0])
        Utility._write_controller_data(l_controllers[0], l_xml)
        Utility._write_interface_data(l_controllers[0], l_xml)
        # print(PrettyFormatAny.form(l_xml, 'AllControllers', 100))
        self.assertEqual(l_xml.find('BaudRate').text, TESTING_SERIAL_BAUD_RATE)
        self.assertEqual(l_xml.find('ByteSize').text, TESTING_SERIAL_BYTE_SIZE)
        self.assertEqual(l_xml.find('Parity').text, TESTING_SERIAL_PARITY)
        self.assertEqual(l_xml.find('RtsCts').text, TESTING_SERIAL_RTS_CTS)
        self.assertEqual(l_xml.find('StopBits').text, TESTING_SERIAL_STOP_BITS)
        self.assertEqual(l_xml.find('Timeout').text, TESTING_SERIAL_TIMEOUT)
        self.assertEqual(l_xml.find('XonXoff').text, TESTING_SERIAL_XON_XOFF)

    def test_04_Family(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_xml = Utility._write_base_device(l_controllers[0])
        Utility._write_controller_data(l_controllers[0], l_xml)
        Utility._write_interface_data(l_controllers[0], l_xml)
        Utility._write_family_data(self.m_pyhouse_obj, l_controllers[0], l_xml)
        # print(PrettyFormatAny.form(l_xml, 'AllControllers', 100))
        self.assertEqual(l_xml.find('Address').text, TESTING_INSTEON_ADDRESS)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM)

    def test_04_OneXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_xml = Utility._write_one_controller_xml(self.m_pyhouse_obj, l_controllers[0])
        # print(PrettyFormatAny.form(l_xml, 'AllControllers', 100))
        self.assertEqual(l_xml.find('Address').text, TESTING_INSTEON_ADDRESS)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM)

    def test_05_AllXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        self.m_pyhouse_obj.House.Controllers = l_controllers
        l_xml = self.m_api.write_all_controllers_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'AllControllers', 100))
        self.assertEqual(l_xml.find('Controller/Address').text, TESTING_INSTEON_ADDRESS)
        self.assertEqual(l_xml.find('Controller/DevCat').text, TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_xml.find('Controller/GroupList').text, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_xml.find('Controller/GroupNumber').text, TESTING_INSTEON_GROUP_NUM)



class C2_JSON(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_controller = self.m_api.read_all_controllers_xml(self.m_pyhouse_obj, self.m_xml.controller_sect, self.m_version)
        l_json = json_tools.encode_json(l_controller)
        # PrettyPrintAny(l_json, 'JSON', 100)

# ## END DBK
