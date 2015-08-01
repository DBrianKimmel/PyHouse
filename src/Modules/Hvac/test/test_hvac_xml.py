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
from Modules.Hvac.hvac_xml import Xml as hvacXML
from Modules.Hvac.test.xml_thermostat import TESTING_THERMOSTAT_NAME, TESTING_THERMOSTAT_ACTIVE, TESTING_THERMOSTAT_KEY, \
        TESTING_THERMOSTAT_ADDRESS, TESTING_THERMOSTAT_COOL_SETPOINT, TESTING_THERMOSTAT_CURRENT_TEMP, \
        TESTING_THERMOSTAT_DEVICE_FAMILY, TESTING_THERMOSTAT_HEAT_SETPOINT, TESTING_THERMOSTAT_MODE, \
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
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Irrigation, None)
        # PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'Device Objs')


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base(self):
        """
        """
        l_xml = self.m_xml.thermostat
        l_obj = hvacXML._read_thermostat_base(l_xml)
        # PrettyPrintAny(l_obj, 'Zone')
        self.assertEqual(l_obj.Name, TESTING_THERMOSTAT_NAME)
        self.assertEqual(l_obj.Active, TESTING_THERMOSTAT_ACTIVE)
        self.assertEqual(l_obj.Key, TESTING_THERMOSTAT_KEY)
        self.assertEqual(l_obj.DeviceFamily, TESTING_THERMOSTAT_DEVICE_FAMILY)
        self.assertEqual(l_obj.Address, TESTING_THERMOSTAT_ADDRESS)

    def test_02_Thermostat(self):
        """
        """
        l_xml = self.m_xml.thermostat
        l_obj = hvacXML._read_thermostat_base(l_xml)
        self.assertEqual(l_obj.Name, 'LawnSystem')

    def test_03_Irrigation(self):
        """
        """
        l_xml = self.m_xml.irrigation_sect
        l_obj = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'XML')
        PrettyPrintAny(l_obj, 'System')
        self.assertEqual(len(l_obj), 2)


class C1_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Zone(self):
        """
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_sys = l_irr[0]
        l_obj = l_sys.Zones[0]
        l_xml = self.m_api._write_one_zone(l_obj)
        PrettyPrintAny(l_obj, 'Zone')
        PrettyPrintAny(l_xml, 'XML')
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Irrigation, None)

    def test_02_System(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_sys = l_irr[0]
        PrettyPrintAny(l_sys, 'System')
        l_xml = self.m_api._write_one_system(l_sys)
        PrettyPrintAny(l_xml, 'XML')
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Irrigation, None)

    def test_03_Irrigation(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_obj = self.m_api.write_irrigation_xml(l_irr)
        PrettyPrintAny(l_obj, 'System')
        self.assertEqual(self.m_pyhouse_obj.House.DeviceOBJs.Irrigation, None)

# ## END DBK
