"""
@name:      PyHouse/Project/src/Modules/Housing/Hvac/test/test_hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

Passed all 5 tests - DBK - 2019-06-04

"""

__updated__ = '2019-06-04'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from test.xml_data import XML_LONG, XML_EMPTY, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import ThermostatData
from Modules.Housing.Hvac.hvac import API as hvacAPI
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = hvacAPI(self.m_pyhouse_obj)
        self.m_thermostat_obj = ThermostatData()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_hvac')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.hvac_sect.tag, 'HvacSection')
        self.assertEqual(self.m_xml.thermostat_sect.tag, 'ThermostatSection')
        self.assertEqual(self.m_xml.thermostat.tag, 'Thermostat')

    def test_02_Load(self):
        """
        """
        l_obj = self.m_api.LoadXml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'A1-02-A - Thermostats', 105))
        self.assertEqual(len(l_obj.Thermostats), 2)


class A2_EmptyXML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

    def test_02_Load(self):
        """
        """
        l_obj = self.m_api.LoadXml(self.m_pyhouse_obj)
        self.assertEqual(len(l_obj.Thermostats), 0)

#  ## END DBK
