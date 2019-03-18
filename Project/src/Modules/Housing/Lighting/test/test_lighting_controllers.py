"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb 21, 2014
@summary:   This module is for testing local node data.

Passed all 24 tests - DBK - 2019-01-10
"""

__updated__ = '2019-03-18'

#  Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Core.data_objects import ControllerData
from Modules.Core.Utilities import json_tools, convert
from Modules.Families.family import API as familyAPI
from Modules.Housing.Lighting.lighting_controllers import XML as controllerXML
from Modules.Housing.Lighting.lighting_xml import LightingXML
from Modules.Core.test.xml_device import \
    TESTING_DEVICE_FAMILY_INSTEON, \
    TESTING_DEVICE_TYPE_0, \
    TESTING_DEVICE_SUBTYPE_0, \
    TESTING_DEVICE_ROOM_NAME_0, \
    TESTING_DEVICE_ROOM_UUID_0, \
    TESTING_DEVICE_COMMENT_0, \
    TESTING_DEVICE_UUID_0, \
    TESTING_DEVICE_COMMENT_1, \
    TESTING_DEVICE_FAMILY_UPB
from Modules.Drivers.Serial.test.xml_serial import \
    TESTING_SERIAL_BAUD_RATE, \
    TESTING_SERIAL_BYTE_SIZE, \
    TESTING_SERIAL_DSR_DTR, \
    TESTING_SERIAL_PARITY, \
    TESTING_SERIAL_RTS_CTS, \
    TESTING_SERIAL_STOP_BITS, \
    TESTING_SERIAL_TIMEOUT, \
    TESTING_SERIAL_XON_XOFF
from Modules.Drivers.USB.test.xml_usb import \
    TESTING_USB_VENDOR, \
    TESTING_USB_PRODUCT
from Modules.Drivers.test.xml_interface import \
    TESTING_INTERFACE_TYPE_SERIAL, \
    TESTING_INTERFACE_PORT_SERIAL, TESTING_INTERFACE_TYPE_USB, TESTING_INTERFACE_PORT_USB
from Modules.Families.Insteon.test.xml_insteon import \
    TESTING_INSTEON_ADDRESS_1, \
    TESTING_INSTEON_DEVCAT_1, \
    TESTING_INSTEON_PRODUCT_KEY_1, \
    TESTING_INSTEON_GROUP_LIST_1, \
    TESTING_INSTEON_GROUP_NUM_1, \
    TESTING_INSTEON_ENGINE_VERSION_1, \
    TESTING_INSTEON_FIRMWARE_VERSION_1
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_DIVISION
from Modules.Housing.Lighting.test.xml_lighting import \
    TESTING_LIGHTING_SECTION
from Modules.Housing.Lighting.test.xml_controllers import \
    TESTING_CONTROLLER_NAME_0, \
    TESTING_CONTROLLER_ACTIVE_0, \
    TESTING_CONTROLLER_KEY_0, \
    TESTING_CONTROLLER_UUID_0, \
    TESTING_CONTROLLER_SECTION, \
    TESTING_CONTROLLER, \
    XML_CONTROLLER_SECTION, \
    TESTING_CONTROLLER_NAME_1, \
    TESTING_CONTROLLER_ACTIVE_1, \
    TESTING_CONTROLLER_KEY_1, \
    TESTING_CONTROLLER_TYPE, \
    TESTING_CONTROLLER_SUBTYPE, \
    TESTING_CONTROLLER_ROOM_NAME_0, \
    TESTING_CONTROLLER_ROOM_UUID_0
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


#  Import PyMh files and modules.
class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.FamilyInformation = self.m_family
        self.m_controller_obj = ControllerData()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_lighting_controllers')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, {})

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.lighting_sect.tag, TESTING_LIGHTING_SECTION)
        self.assertEqual(self.m_xml.controller_sect.tag, TESTING_CONTROLLER_SECTION)
        self.assertEqual(self.m_xml.controller.tag, TESTING_CONTROLLER)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_xml = XML_CONTROLLER_SECTION
        # print(l_xml)
        self.assertEqual(l_xml[:19], '<ControllerSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_CONTROLLER_SECTION)
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A Parsed'))
        self.assertEqual(l_xml.tag, TESTING_CONTROLLER_SECTION)

    def test_03_Family(self):
        self.assertEqual(self.m_family['Insteon'].Name, 'Insteon')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseDevice0(self):
        """Read Base Device
        Skip testing of room coords
        """
        l_xml = self.m_xml.controller_sect[0]
        # print(PrettyFormatAny.form(l_xml, 'B1-01-A - Base Device'))
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-01-B - Base Device'))
        self.assertEqual(l_obj.Name, TESTING_CONTROLLER_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_CONTROLLER_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_CONTROLLER_ACTIVE_0)
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT_0)
        self.assertEqual(l_obj.UUID, TESTING_CONTROLLER_UUID_0)
        # Plus Device Info
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(str(l_obj.DeviceType), TESTING_CONTROLLER_TYPE)
        self.assertEqual(str(l_obj.DeviceSubType), TESTING_CONTROLLER_SUBTYPE)
        # Plus Room Info
        self.assertEqual(l_obj.RoomName, TESTING_CONTROLLER_ROOM_NAME_0)
        self.assertEqual(l_obj.RoomUUID, TESTING_CONTROLLER_ROOM_UUID_0)

    def test_02_BaseDevice1(self):
        """Read Base Device
        Skip testing of room coords
        """
        l_xml = self.m_xml.controller_sect[1]
        # print(PrettyFormatAny.form(l_xml, 'B1-02-A - Base Device'))
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - Base Device'))
        self.assertEqual(l_obj.Name, TESTING_CONTROLLER_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_CONTROLLER_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_CONTROLLER_ACTIVE_1)
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT_1)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(str(l_obj.DeviceType), TESTING_DEVICE_TYPE_0)
        self.assertEqual(str(l_obj.DeviceSubType), TESTING_DEVICE_SUBTYPE_0)
        self.assertEqual(l_obj.RoomName, TESTING_DEVICE_ROOM_NAME_0)
        self.assertEqual(l_obj.RoomUUID, TESTING_DEVICE_ROOM_UUID_0)

    def test_03_Controller0(self):
        """Read Controller 0 Insteon Serial
        """
        l_xml = self.m_xml.controller_sect[0]
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        l_obj = controllerXML()._read_controller_data(self.m_pyhouse_obj, l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - Controller'))
        self.assertEqual(l_obj.InterfaceType, TESTING_INTERFACE_TYPE_SERIAL)
        self.assertEqual(l_obj.Port, TESTING_INTERFACE_PORT_SERIAL)

    def test_04_Controller1(self):
        """Read Controller 1 UPB USB
        """
        l_xml = self.m_xml.controller_sect[1]
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        l_obj = controllerXML()._read_controller_data(self.m_pyhouse_obj, l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-04-A - Controller'))
        self.assertEqual(l_obj.InterfaceType, TESTING_INTERFACE_TYPE_USB)
        self.assertEqual(l_obj.Port, TESTING_INTERFACE_PORT_USB)

    def test_05_Interface0(self):
        """Read Controller Interface.
        """
        l_xml = self.m_xml.controller_sect[0]
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        l_obj = controllerXML()._read_controller_data(self.m_pyhouse_obj, l_obj, l_xml)
        controllerXML()._read_interface_data(self.m_pyhouse_obj, l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-05-A - Interface'))
        self.assertEqual(str(l_obj.BaudRate), TESTING_SERIAL_BAUD_RATE)
        self.assertEqual(str(l_obj.ByteSize), TESTING_SERIAL_BYTE_SIZE)
        self.assertEqual(str(l_obj.DsrDtr), TESTING_SERIAL_DSR_DTR)
        self.assertEqual(l_obj.Parity, TESTING_SERIAL_PARITY)
        self.assertEqual(str(l_obj.RtsCts), TESTING_SERIAL_RTS_CTS)
        self.assertEqual(str(l_obj.StopBits), TESTING_SERIAL_STOP_BITS)
        self.assertEqual(str(l_obj.Timeout), TESTING_SERIAL_TIMEOUT)
        self.assertEqual(str(l_obj.XonXoff), TESTING_SERIAL_XON_XOFF)

    def test_06_Interface1(self):
        """Read Controller Interface.
        """
        l_xml = self.m_xml.controller_sect[1]
        # print(PrettyFormatAny.form(l_xml, 'B1-06-A - Interface'))
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        l_obj = controllerXML()._read_controller_data(self.m_pyhouse_obj, l_obj, l_xml)
        controllerXML()._read_interface_data(self.m_pyhouse_obj, l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-06-B - Interface'))
        self.assertEqual(str(l_obj.Vendor), TESTING_USB_VENDOR)
        self.assertEqual(str(l_obj.Product), TESTING_USB_PRODUCT)

    def test_07_Family0(self):
        """Read controller family
        """
        l_xml = self.m_xml.controller_sect[0]
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        controllerXML()._read_controller_data(self.m_pyhouse_obj, l_obj, l_xml)
        controllerXML()._read_interface_data(self.m_pyhouse_obj, l_obj, l_xml)
        LightingXML()._read_family_data(self.m_pyhouse_obj, l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-07-A - Family'))
        self.assertEqual(convert.int2dotted_hex(l_obj.InsteonAddress, 3), TESTING_INSTEON_ADDRESS_1)
        self.assertEqual(convert.int2dotted_hex(l_obj.DevCat, 2), TESTING_INSTEON_DEVCAT_1)
        self.assertEqual(convert.int2dotted_hex(l_obj.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY_1)
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST_1)
        self.assertEqual(str(l_obj.GroupNumber), TESTING_INSTEON_GROUP_NUM_1)

    def test_08_Family1(self):
        """Read controller family
        """
        l_xml = self.m_xml.controller_sect[0]
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        controllerXML()._read_controller_data(self.m_pyhouse_obj, l_obj, l_xml)
        controllerXML()._read_interface_data(self.m_pyhouse_obj, l_obj, l_xml)
        LightingXML()._read_family_data(self.m_pyhouse_obj, l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-08-A - Family'))
        self.assertEqual(convert.int2dotted_hex(l_obj.InsteonAddress, 3), TESTING_INSTEON_ADDRESS_1)
        self.assertEqual(convert.int2dotted_hex(l_obj.DevCat, 2), TESTING_INSTEON_DEVCAT_1)
        self.assertEqual(convert.int2dotted_hex(l_obj.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY_1)
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST_1)
        self.assertEqual(str(l_obj.GroupNumber), TESTING_INSTEON_GROUP_NUM_1)

    def test_09_OneController0(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = controllerXML()._read_one_controller_xml(self.m_pyhouse_obj, self.m_xml.controller)
        # print(PrettyFormatAny.form(l_obj, 'B1-05-A - OneController', 100))
        self.assertEqual(l_obj.Name, TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_obj.Active, (TESTING_CONTROLLER_ACTIVE_0 == 'True'))
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT_0)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_obj.DeviceType, int(TESTING_DEVICE_TYPE_0))
        self.assertEqual(l_obj.DeviceSubType, int(TESTING_DEVICE_SUBTYPE_0))
        self.assertEqual(l_obj.RoomName, TESTING_CONTROLLER_ROOM_NAME_0)
        self.assertEqual(l_obj.InterfaceType, TESTING_INTERFACE_TYPE_SERIAL)
        self.assertEqual(l_obj.Port, TESTING_INTERFACE_PORT_SERIAL)
        self.assertEqual(l_obj.BaudRate, int(TESTING_SERIAL_BAUD_RATE))
        self.assertEqual(l_obj.ByteSize, int(TESTING_SERIAL_BYTE_SIZE))
        self.assertEqual(l_obj.Parity, TESTING_SERIAL_PARITY)
        self.assertEqual(str(l_obj.RtsCts), TESTING_SERIAL_RTS_CTS)
        self.assertEqual(l_obj.StopBits, float(TESTING_SERIAL_STOP_BITS))
        self.assertEqual(l_obj.Timeout, float(TESTING_SERIAL_TIMEOUT))
        self.assertEqual(l_obj.XonXoff, TESTING_SERIAL_XON_XOFF == 'True')
        self.assertEqual(convert.int2dotted_hex(l_obj.InsteonAddress, 3), TESTING_INSTEON_ADDRESS_1)
        self.assertEqual(convert.int2dotted_hex(l_obj.DevCat, 2), TESTING_INSTEON_DEVCAT_1)
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST_1)
        self.assertEqual(str(l_obj.GroupNumber), TESTING_INSTEON_GROUP_NUM_1)

    def test_10_OneController1(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = controllerXML()._read_one_controller_xml(self.m_pyhouse_obj, self.m_xml.controller)
        # print(PrettyFormatAny.form(l_obj, 'B1-05-A - OneController', 100))
        self.assertEqual(l_obj.Name, TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_obj.Active, (TESTING_CONTROLLER_ACTIVE_0 == 'True'))
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT_0)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_obj.DeviceType, int(TESTING_DEVICE_TYPE_0))
        self.assertEqual(l_obj.DeviceSubType, int(TESTING_DEVICE_SUBTYPE_0))
        self.assertEqual(l_obj.RoomName, TESTING_CONTROLLER_ROOM_NAME_0)
        self.assertEqual(l_obj.InterfaceType, TESTING_INTERFACE_TYPE_SERIAL)
        self.assertEqual(l_obj.Port, TESTING_INTERFACE_PORT_SERIAL)
        self.assertEqual(l_obj.BaudRate, int(TESTING_SERIAL_BAUD_RATE))
        self.assertEqual(l_obj.ByteSize, int(TESTING_SERIAL_BYTE_SIZE))
        self.assertEqual(l_obj.Parity, TESTING_SERIAL_PARITY)
        self.assertEqual(str(l_obj.RtsCts), TESTING_SERIAL_RTS_CTS)
        self.assertEqual(l_obj.StopBits, float(TESTING_SERIAL_STOP_BITS))
        self.assertEqual(l_obj.Timeout, float(TESTING_SERIAL_TIMEOUT))
        self.assertEqual(l_obj.XonXoff, TESTING_SERIAL_XON_XOFF == 'True')
        self.assertEqual(convert.int2dotted_hex(l_obj.InsteonAddress, 3), TESTING_INSTEON_ADDRESS_1)
        self.assertEqual(convert.int2dotted_hex(l_obj.DevCat, 2), TESTING_INSTEON_DEVCAT_1)
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST_1)
        self.assertEqual(str(l_obj.GroupNumber), TESTING_INSTEON_GROUP_NUM_1)

    def test_11_AllControllers(self):
        """Read all controllers.
        """
        l_objs = controllerXML().read_all_controllers_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_objs, 'B1-06-A - AllControllers'))
        # print(PrettyFormatAny.form(l_objs[0], 'B1-06-B - AllControllers'))
        # print(PrettyFormatAny.form(l_objs[1], 'B1-06-C - AllControllers'))
        self.assertEqual(len(l_objs), 3)
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
        self.m_controllers = controllerXML().read_all_controllers_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Lighting.Controllers = self.m_controllers

    def test_01_Base(self):
        """ Write out the XML file for the Base controller
        """
        l_xml = LightingXML()._write_base_device(self.m_pyhouse_obj, self.m_controllers[0])
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - Base'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_CONTROLLER_KEY_0)
        self.assertEqual(bool(l_xml.attrib['Active']), TESTING_CONTROLLER_ACTIVE_0 == 'True')
        self.assertEqual(l_xml.find('UUID').text, TESTING_CONTROLLER_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_DEVICE_TYPE_0)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_DEVICE_SUBTYPE_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_CONTROLLER_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_CONTROLLER_ROOM_UUID_0)

    def test_02_Controller(self):
        """ Write out the XML file for the Base + Controller
        """
        l_xml = LightingXML()._write_base_device(self.m_pyhouse_obj, self.m_controllers[0])
        controllerXML()._write_controller_data(self.m_controllers[0], l_xml)
        # print(PrettyFormatAny.form(l_xml, 'C1-02-A - Base'))
        self.assertEqual(l_xml.find('InterfaceType').text, TESTING_INTERFACE_TYPE_SERIAL)
        self.assertEqual(l_xml.find('Port').text, TESTING_INTERFACE_PORT_SERIAL)

    def test_03_Interface(self):
        """ Write out the XML file for the location section
        """
        l_xml = LightingXML()._write_base_device(self.m_pyhouse_obj, self.m_controllers[0])
        controllerXML()._write_controller_data(self.m_controllers[0], l_xml)
        controllerXML()._write_interface_data(self.m_controllers[0], l_xml)
        # print(PrettyFormatAny.form(l_xml, 'C1-03-A - w/ Interface', 100))
        l_xml = l_xml.find('Serial')
        self.assertEqual(l_xml.find('BaudRate').text, TESTING_SERIAL_BAUD_RATE)
        self.assertEqual(l_xml.find('ByteSize').text, TESTING_SERIAL_BYTE_SIZE)
        self.assertEqual(l_xml.find('DsrDtr').text, TESTING_SERIAL_DSR_DTR)
        self.assertEqual(l_xml.find('Parity').text, TESTING_SERIAL_PARITY)
        self.assertEqual(l_xml.find('RtsCts').text, TESTING_SERIAL_RTS_CTS)
        self.assertEqual(l_xml.find('StopBits').text, TESTING_SERIAL_STOP_BITS)
        self.assertEqual(l_xml.find('Timeout').text, TESTING_SERIAL_TIMEOUT)
        self.assertEqual(l_xml.find('XonXoff').text, TESTING_SERIAL_XON_XOFF)

    def test_04_Family(self):
        """ Write out the XML file for the location section
        """
        l_xml = LightingXML()._write_base_device(self.m_pyhouse_obj, self.m_controllers[0])
        controllerXML()._write_controller_data(self.m_controllers[0], l_xml)
        controllerXML()._write_interface_data(self.m_controllers[0], l_xml)
        LightingXML()._write_family_data(self.m_pyhouse_obj, self.m_controllers[0], l_xml)
        # print(PrettyFormatAny.form(l_xml, 'C1-04-A - w/ Family', 100))
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT_1)
        self.assertEqual(l_xml.find('EngineVersion').text, TESTING_INSTEON_ENGINE_VERSION_1)
        self.assertEqual(l_xml.find('FirmwareVersion').text, TESTING_INSTEON_FIRMWARE_VERSION_1)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST_1)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM_1)
        self.assertEqual(l_xml.find('InsteonAddress').text, TESTING_INSTEON_ADDRESS_1)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY_1)

    def test_05_OneXml(self):
        """ Write out the XML file for the location section
        """
        l_xml = controllerXML()._write_one_controller_xml(self.m_pyhouse_obj, self.m_controllers[0])
        # print(PrettyFormatAny.form(l_xml, 'C1-05-A - AllControllers', 100))
        self.assertEqual(l_xml.find('InsteonAddress').text, TESTING_INSTEON_ADDRESS_1)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT_1)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST_1)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM_1)

    def test_06_AllXml(self):
        """ Write out the XML file for the location section
        """
        l_xml = controllerXML().write_all_controllers_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'C1-06-A - AllControllers', 100))
        self.assertEqual(l_xml.find('Controller/InsteonAddress').text, TESTING_INSTEON_ADDRESS_1)
        self.assertEqual(l_xml.find('Controller/DevCat').text, TESTING_INSTEON_DEVCAT_1)
        self.assertEqual(l_xml.find('Controller/GroupList').text, TESTING_INSTEON_GROUP_LIST_1)
        self.assertEqual(l_xml.find('Controller/GroupNumber').text, TESTING_INSTEON_GROUP_NUM_1)


class C2_JSON(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_controllers = controllerXML().read_all_controllers_xml(self.m_pyhouse_obj)

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_json = json_tools.encode_json(self.m_controllers[0])
        # print('C2-01-A - ', l_json)
        # print(PrettyFormatAny.form(l_json, 'C2-01-A - AllControllers', 100))

#  ## END DBK
