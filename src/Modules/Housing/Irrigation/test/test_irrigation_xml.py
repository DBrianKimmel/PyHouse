"""
@name:      PyHouse/src/Modules/Irrigation/test/test_irrigation_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 30, 2015
@summary:

Passed all 8 tests - DBK - 2016-08-24

"""
from Modules.Housing.Irrigation.test.xml_irrigation import TESTING_IRRIGATION_ZONE_NAME_0_0, \
    TESTING_IRRIGATION_SYSTEM_NAME_0, TESTING_IRRIGATION_ZONE_KEY_0_0, TESTING_IRRIGATION_ZONE_ACTIVE_0_0, \
    TESTING_IRRIGATION_ZONE_COMMENT_0_0, TESTING_IRRIGATION_ZONE_DURATION_0_0

__updated__ = '2016-08-24'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Housing.Irrigation.irrigation_xml import Xml as irrigationXml
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = irrigationXml


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml.irrigation_sect, 'A1-01-A - Irrigation'))
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, None)

    def test_02_XML(self):
        # print(PrettyFormatAny.form(self.m_xml.irrigation_system, 'A1-02-A - Irrigation'))
        # print(PrettyFormatAny.form(self.m_xml.irrigation_zone, 'A1-02-B - Irrigation'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.irrigation_sect.tag, 'IrrigationSection')
        self.assertEqual(self.m_xml.irrigation_system.tag, 'IrrigationSystem')
        self.assertEqual(self.m_xml.irrigation_zone.tag, 'Zone')



class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Zone(self):
        """
        """
        l_xml = self.m_xml.irrigation_zone
        l_obj = self.m_api._read_one_zone(l_xml)
        print(PrettyFormatAny.form(l_obj, 'B1-01-A - Zone'))
        self.assertEqual(str(l_obj.Name), TESTING_IRRIGATION_ZONE_NAME_0_0)
        self.assertEqual(str(l_obj.Key), TESTING_IRRIGATION_ZONE_KEY_0_0)
        self.assertEqual(str(l_obj.Active), TESTING_IRRIGATION_ZONE_ACTIVE_0_0)
        self.assertEqual(str(l_obj.Comment), TESTING_IRRIGATION_ZONE_COMMENT_0_0)
        self.assertEqual(str(l_obj.Duration), TESTING_IRRIGATION_ZONE_DURATION_0_0)

    def test_02_System(self):
        """
        """
        l_xml = self.m_xml.irrigation_system
        l_obj = self.m_api._read_one_irrigation_system(l_xml)
        print(PrettyFormatAny.form(l_obj, 'B1-01-A - System'))
        self.assertEqual(l_obj.Name, TESTING_IRRIGATION_SYSTEM_NAME_0)

    def test_03_Irrigation(self):
        """
        """
        l_xml = self.m_xml.irrigation_sect
        l_obj = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'B1-03-A - Irrigation'))
        self.assertEqual(len(l_obj), 3)


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
        print(PrettyFormatAny.form(l_obj, 'C1-01-A - Zone'))
        print(PrettyFormatAny.form(l_xml, 'C1-01-B - Zone'))
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, None)

    def test_02_System(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_sys = l_irr[0]
        l_xml = self.m_api._write_one_system(l_sys)
        print(PrettyFormatAny.form(l_xml, 'C1-02-A - System'))
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, None)

    def test_03_Irrigation(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_obj = self.m_api.write_irrigation_xml(l_irr)
        print(PrettyFormatAny.form(l_obj, 'C1-03-A - Irrigate'))
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, None)

# ## END DBK
