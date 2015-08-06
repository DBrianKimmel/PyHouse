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
        XML_DEVICE, \
        TESTING_DEVICE_COMMENT, \
        TESTING_DEVICE_FAMILY, \
        TESTING_DEVICE_ROOM_NAME
from Modules.Hvac.test.xml_thermostat import \
        TESTING_THERMOSTAT_NAME, \
        TESTING_THERMOSTAT_ACTIVE, \
        TESTING_THERMOSTAT_KEY, \
        TESTING_THERMOSTAT_ADDRESS, \
        TESTING_THERMOSTAT_COOL_SETPOINT, \
        TESTING_THERMOSTAT_CURRENT_TEMP, \
        TESTING_THERMOSTAT_DEVICE_FAMILY, \
        TESTING_THERMOSTAT_HEAT_SETPOINT, \
        TESTING_THERMOSTAT_MODE, \
        TESTING_THERMOSTAT_SCALE
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


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
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Hvac, None)


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseDevice(self):
        l_xml = self.m_xml.thermostat
        l_obj = Utility._read_thermostat_base(l_xml)
        self.assertEqual(l_obj.Name, TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_obj.Active, bool(TESTING_THERMOSTAT_ACTIVE == True))
        self.assertEqual(l_obj.Key, int(TESTING_THERMOSTAT_KEY))
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_obj.DeviceFamily, TESTING_THERMOSTAT_DEVICE_FAMILY)
        self.assertEqual(l_obj.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_02_Thermostat(self):
        l_xml = self.m_xml.thermostat
        l_obj = Utility._read_thermostat_base(l_xml)
        Utility._read_thermostat_data(l_obj, l_xml)
        self.assertEqual(l_obj.Name, TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_obj.CoolSetPoint, float(TESTING_THERMOSTAT_COOL_SETPOINT))
        self.assertEqual(l_obj.HeatSetPoint, float(TESTING_THERMOSTAT_HEAT_SETPOINT))
        self.assertEqual(l_obj.ThermostatMode, TESTING_THERMOSTAT_MODE)
        self.assertEqual(l_obj.ThermostatScale, TESTING_THERMOSTAT_SCALE)

    def test_03_Family(self):
        l_xml = self.m_xml.thermostat
        l_obj = Utility._read_thermostat_base(l_xml)
        Utility._read_thermostat_data(l_obj, l_xml)
        l_ret = Utility._read_family_data(self.m_pyhouse_obj, l_obj, l_xml)
        print(l_ret)
        PrettyPrintAny(l_xml, 'XML')
        PrettyPrintAny(l_obj, 'System')
        self.assertEqual(l_obj.Address, '2')

    def test_04_AllThermostats(self):
        pass


class C1_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseDevice(self):
        """
        """
        l_xml = self.m_xml.thermostat_sect
        l_obj = Utility._read_thermostat_base(l_xml)
        # PrettyPrintAny(l_xml, 'XML Thermostat Device')
        l_ret = Utility._write_thermostat_base('Thermostat', l_obj)
        # PrettyPrintAny(l_ret, 'Base Thermostat Device')
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Hvac, None)

    def test_02_Thermostat(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_xml = self.m_xml.thermostat_sect
        l_obj = Utility._read_thermostat_base(l_xml)
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_sys = l_irr[0]
        # PrettyPrintAny(l_sys, 'System')
        l_xml = self.m_api._write_one_system(l_sys)
        # PrettyPrintAny(l_xml, 'XML')
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Irrigation, None)

    def test_03_Family(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_xml = self.m_xml.thermostat_sect
        l_obj = Utility._read_thermostat_base(l_xml)
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_obj = self.m_api.write_irrigation_xml(l_irr)
        # PrettyPrintAny(l_obj, 'System')
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Irrigation, None)

# ## END DBK
