"""
@name:      PyHouse/src/Modules/Drivers/USB/test/test_USB_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 30, 2015
@Summary:

Passed all 3 tests - DBK - 2018-02-13

"""

__updated__ = '2018-02-13'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Drivers.USB.USB_xml import XML as usbXML
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import ControllerData
from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.Core.Utilities.device_tools import stuff_new_attrs
from Modules.Drivers.USB.test.xml_usb import TESTING_USB_VENDOR, TESTING_USB_PRODUCT
from Modules.Housing.Lighting.test.xml_controllers import \
    TESTING_CONTROLLER_NAME_1, \
    TESTING_CONTROLLER_KEY_1, \
    TESTING_CONTROLLER_ACTIVE_1
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_version = '1.4.0'
        self.m_api = deviceXML


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_USB_xml')


class B1_Read(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Interface(self):
        l_ctlr = self.m_xml.controller_sect[1]
        l_device = ControllerData()
        l_obj = self.m_api.read_base_device_object_xml(self.m_pyhouse_obj, l_device, l_ctlr)
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - L L'))
        L_interface = usbXML.read_interface_xml(l_ctlr)
        stuff_new_attrs(l_obj, L_interface)
        # print(PrettyFormatAny.form(l_obj, 'B1-01-B - L L'))
        self.assertEqual(l_obj.Vendor, int(TESTING_USB_VENDOR))
        self.assertEqual(l_obj.Product, int(TESTING_USB_PRODUCT))


class B2_Write(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Interface(self):
        l_ctlr = self.m_xml.controller_sect[1]
        l_device = ControllerData()
        l_obj = self.m_api.read_base_device_object_xml(self.m_pyhouse_obj, l_device, l_ctlr)
        L_interface = usbXML.read_interface_xml(l_ctlr)
        stuff_new_attrs(l_obj, L_interface)
        # print(PrettyFormatAny.form(l_obj, 'B2-01-A - Controller xml'))
        l_xml = self.m_api.write_base_device_object_xml('TestController', l_obj)
        usbXML.write_interface_xml(l_xml, l_obj)
        # print(PrettyFormatAny.form(l_xml, 'B2-01-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_CONTROLLER_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_CONTROLLER_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_CONTROLLER_ACTIVE_1)
        self.assertEqual(l_xml.find('Vendor').text, TESTING_USB_VENDOR)
        self.assertEqual(l_xml.find('Product').text, TESTING_USB_PRODUCT)

# ## END DBK
