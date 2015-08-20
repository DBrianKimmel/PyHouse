"""
@name:      PyHouse/src/Modules/Hvac/test/test_hvac_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Hvac.hvac_xml import Utility, XML as hvacXML
from Modules.Core.test.xml_device import \
        TESTING_DEVICE_COMMENT, \
        TESTING_DEVICE_ROOM_NAME, \
        TESTING_DEVICE_FAMILY_INSTEON
from Modules.Hvac.test.xml_hvac import \
        TESTING_THERMOSTAT_NAME, \
        TESTING_THERMOSTAT_ACTIVE, \
        TESTING_THERMOSTAT_KEY, \
        TESTING_THERMOSTAT_COOL_SETPOINT, \
        TESTING_THERMOSTAT_DEVICE_FAMILY, \
        TESTING_THERMOSTAT_HEAT_SETPOINT, \
        TESTING_THERMOSTAT_MODE, \
        TESTING_THERMOSTAT_SCALE
from Modules.Families.Insteon.test.xml_insteon import \
        TESTING_INSTEON_ADDRESS, \
        TESTING_INSTEON_DEVCAT, \
        TESTING_INSTEON_GROUP_LIST, \
        TESTING_INSTEON_GROUP_NUM, \
        TESTING_INSTEON_PRODUCT_KEY
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Core import conversions
from Modules.Drivers import Ethernet


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Hvac, None)
        # print(PrettyFormatAny.form(self.m_xml.thermostat_sect, 'Thermostat'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'Family'))


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseDevice(self):
        """Read the base device XML
        """
        l_xml = self.m_xml.thermostat
        l_obj = Utility._read_thermostat_base(l_xml)
        self.assertEqual(l_obj.Name, TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_obj.Active, TESTING_THERMOSTAT_ACTIVE == 'True')
        self.assertEqual(l_obj.Key, int(TESTING_THERMOSTAT_KEY))
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_obj.DeviceFamily, TESTING_THERMOSTAT_DEVICE_FAMILY)
        self.assertEqual(l_obj.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_02_Thermostat(self):
        """Read the thermostat specific data.
        """
        l_xml = self.m_xml.thermostat
        l_obj = Utility._read_thermostat_base(l_xml)
        Utility._read_thermostat_data(l_obj, l_xml)
        self.assertEqual(l_obj.Name, TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_obj.CoolSetPoint, float(TESTING_THERMOSTAT_COOL_SETPOINT))
        self.assertEqual(l_obj.HeatSetPoint, float(TESTING_THERMOSTAT_HEAT_SETPOINT))
        self.assertEqual(l_obj.ThermostatMode, TESTING_THERMOSTAT_MODE)
        self.assertEqual(l_obj.ThermostatScale, TESTING_THERMOSTAT_SCALE)

    def test_03_Family(self):
        """Read and add the family specific parts.
        """
        l_xml = self.m_xml.thermostat
        l_obj = Utility._read_thermostat_base(l_xml)
        Utility._read_thermostat_data(l_obj, l_xml)
        Utility._read_family_data(self.m_pyhouse_obj, l_obj, l_xml)
        self.assertEqual(conversions.int2dotted_hex(l_obj.InsteonAddress, 3), TESTING_INSTEON_ADDRESS)
        self.assertEqual(conversions.int2dotted_hex(l_obj.DevCat, 2), TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_obj.GroupNumber, int(TESTING_INSTEON_GROUP_NUM))
        self.assertEqual(conversions.int2dotted_hex(l_obj.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY)

    def test_04_OneThermostat(self):
        """Read one thermostat entirely.
        """
        l_obj = Utility._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        self.assertEqual(l_obj.Name, TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_obj.CoolSetPoint, float(TESTING_THERMOSTAT_COOL_SETPOINT))
        self.assertEqual(conversions.int2dotted_hex(l_obj.InsteonAddress, 3), TESTING_INSTEON_ADDRESS)

    def test_05_AllThermostats(self):
        """Read all the thermostats on file.
        """
        l_objs = hvacXML.read_hvac_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_objs, 'All Thermostats'))
        self.assertEqual(len(l_objs), 1)
        self.assertEqual(l_objs[0].Name, TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_objs[0].CoolSetPoint, float(TESTING_THERMOSTAT_COOL_SETPOINT))


class C1_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseDevice(self):
        """Write the base device.
        """
        l_obj = Utility._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        # print(PrettyFormatAny.form(l_obj, 'Thermostat Base Obj'))
        l_xml = Utility._write_thermostat_base('Thermostat', l_obj)
        self.assertEqual(self.m_pyhouse_obj.House.Hvac, None)
        self.assertEqual(l_xml.attrib['Name'], TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_xml.attrib['Key'], TESTING_THERMOSTAT_KEY)
        self.assertEqual(l_xml.attrib['Active'], TESTING_THERMOSTAT_ACTIVE)
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_DEVICE_ROOM_NAME)

    def test_02_Thermostat(self):
        """ Write the thermostat specific data to XML
        """
        l_obj = Utility._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        l_xml = Utility._write_thermostat_base('Thermostat', l_obj)
        Utility._write_thermostat_data(l_xml, l_obj)
        self.assertEqual(self.m_pyhouse_obj.House.Hvac, None)
        self.assertEqual(l_xml.attrib['Name'], TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_xml.attrib['Key'], TESTING_THERMOSTAT_KEY)
        self.assertEqual(l_xml.attrib['Active'], TESTING_THERMOSTAT_ACTIVE)
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('CoolSetPoint').text, TESTING_THERMOSTAT_COOL_SETPOINT)

    def test_03_Family(self):
        """Write family data to XML
        """
        l_obj = Utility._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        l_xml = Utility._write_thermostat_base('Thermostat', l_obj)
        Utility._write_thermostat_data(l_xml, l_obj)
        Utility._write_family_data(self.m_pyhouse_obj, l_obj, l_xml)
        # print(PrettyFormatAny.form(l_xml, 'W/ Family'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_xml.find('Address').text, TESTING_INSTEON_ADDRESS)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY)

    def test_04_OneThermostat(self):
        """Write one complete thermostat
        """
        l_obj = Utility._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        l_xml = Utility._write_one_thermostat_xml(self.m_pyhouse_obj, l_obj)
        self.assertEqual(self.m_pyhouse_obj.House.Hvac, None)
        self.assertEqual(l_xml.attrib['Name'], TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_xml.attrib['Key'], TESTING_THERMOSTAT_KEY)
        self.assertEqual(l_xml.attrib['Active'], TESTING_THERMOSTAT_ACTIVE)
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('CoolSetPoint').text, TESTING_THERMOSTAT_COOL_SETPOINT)
        self.assertEqual(l_xml.find('Address').text, TESTING_INSTEON_ADDRESS)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY)

    def test_05_All(self):
        """ Write all thermostats
        """
        l_objs = hvacXML.read_hvac_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Hvac = l_objs
        l_xml = ET.Element('HvacSection')
        l_xml = hvacXML.write_hvac_xml(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_xml, 'All Thermostats'))
        self.assertEqual(l_xml.find('Thermostat/Comment').text, TESTING_DEVICE_COMMENT)

# ## END DBK
