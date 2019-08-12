"""
@name:      PyHouse/src/Modules/families/UPB/_test/test_UPB_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   This module is for testing UPB devices.

Passed all 1 tests - DBK - 2015-08-15

"""

__updated__ = '2017-01-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families.UPB.UPB_device import API as upbDeviceAPI
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_SetupL(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = upbDeviceAPI(self.m_pyhouse_obj)

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.thermostat_sect.tag, 'ThermostatSection', 'XML - No Thermostat section')
        self.assertEqual(self.m_xml.thermostat.tag, 'Thermostat', 'XML - No Thermostat Entry')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Light section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light Entry')

    def Xtest_02_ReadOneLightXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_entry = self.m_thermostat_api._read_one_thermostat_xml(self.m_thermostat_xml, self.m_pyhouse_obj)
        self.assertEqual(l_entry.Active, True, 'Bad Active')
        self.assertEqual(l_entry.Name, 'Test Thermostat One', 'Bad Name')

        l_light = self.m_light_api.read_one_light_xml(self.m_light_xml)
        l_insteon_obj = self.m_api.extract_device_xml(l_light, self.m_light_xml)
        self.assertEqual(l_light.Name, 'Test LR Overhead', 'Bad Name')
        self.assertEqual(l_light.Key, 0, 'Bad Key')
        self.assertEqual(l_light.Active, True, 'Bad Active')
        self.assertEqual(l_light.UUID, 'ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2', 'Bad UUID')
        self.assertEqual(l_light.InsteonAddress, 1122867, 'Bad Address')

# ## END DBK
