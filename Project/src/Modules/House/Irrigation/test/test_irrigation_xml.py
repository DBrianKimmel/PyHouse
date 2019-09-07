"""
@name:      PyHouse/src/Modules/Irrigation/_test/test_irrigation_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 30, 2015
@summary:

Passed all 11 tests - DBK - 2018-02-10

"""

__updated__ = '2018-02-11'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import json_tools
from Modules.Housing.Irrigation.irrigation_xml import Xml as irrigationXml
from Modules.Housing.Irrigation.test.xml_irrigation import \
    XML_IRRIGATION, \
    TESTING_IRRIGATION_SECTION, \
    TESTING_IRRIGATION_SYSTEM_NAME_0, \
    TESTING_IRRIGATION_ZONE_NAME_0_0, \
    TESTING_IRRIGATION_ZONE_KEY_0_0, \
    TESTING_IRRIGATION_ZONE_ACTIVE_0_0, \
    TESTING_IRRIGATION_ZONE_COMMENT_0_0, \
    TESTING_IRRIGATION_ZONE_DURATION_0_0, \
    TESTING_IRRIGATION_ZONE_EMITTER_COUNT_0_0, \
    TESTING_IRRIGATION_ZONE_EMITTER_TYPE_0_0, \
    TESTING_IRRIGATION_ZONE_NEXT_0_0, \
    TESTING_IRRIGATION_ZONE_PREV_0_0, \
    TESTING_IRRIGATION_ZONE_RATE_0_0, \
    TESTING_IRRIGATION_ZONE_START_TIME_0_0, \
    TESTING_IRRIGATION_SYSTEM_COMMENT_0, \
    TESTING_IRRIGATION_SYSTEM_MASTER_VALVE_0, \
    TESTING_IRRIGATION_SYSTEM_KEY_0, \
    TESTING_IRRIGATION_SYSTEM_ACTIVE_0, \
    TESTING_IRRIGATION_SYSTEM_PUMP_RELAY_0, \
    TESTING_IRRIGATION_SYSTEM_FIRST_ZONE_0, \
    TESTING_IRRIGATION_SYSTEM_TYPE_0, \
    TESTING_IRRIGATION_SYSTEM_NAME_1, \
    TESTING_IRRIGATION_SYSTEM_KEY_1, \
    TESTING_IRRIGATION_SYSTEM_ACTIVE_1, \
    TESTING_IRRIGATION_SYSTEM_NAME_2, \
    TESTING_IRRIGATION_SYSTEM_KEY_2, \
    TESTING_IRRIGATION_SYSTEM_ACTIVE_2
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = irrigationXml

    def jsonPair(self, p_json, p_key):
        """ Extract key, value from json
        """
        l_json = json_tools.decode_json_unicode(p_json)
        try:
            l_val = l_json[p_key]
        except (KeyError, ValueError) as e_err:
            l_val = 'ERRor on JsonPair for key "{}"  {} {}'.format(p_key, e_err, l_json)
            print(l_val)
        return l_val


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_irrigation_xml')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Irrigation is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml.irrigation_sect, 'A1-01-A - Irrigation'))
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, {})

    def test_02_XML(self):
        # print(PrettyFormatAny.form(self.m_xml.irrigation_system, 'A1-02-A - Irrigation'))
        # print(PrettyFormatAny.form(self.m_xml.irrigation_zone, 'A1-02-B - Irrigation'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.irrigation_sect.tag, 'IrrigationSection')
        self.assertEqual(self.m_xml.irrigation_system.tag, 'System')
        self.assertEqual(self.m_xml.irrigation_zone.tag, 'Zone')


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_IRRIGATION
        # print('A2-01-A - Raw', l_raw)
        self.assertEqual(l_raw[:19], '<IrrigationSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_IRRIGATION)
        # print('A2-02-A - Parsed', l_xml)
        self.assertEqual(l_xml.tag, TESTING_IRRIGATION_SECTION)


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Zone(self):
        """
        """
        l_xml = self.m_xml.irrigation_zone
        l_obj = self.m_api._read_one_zone(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - Zone'))
        self.assertEqual(str(l_obj.Name), TESTING_IRRIGATION_ZONE_NAME_0_0)
        self.assertEqual(str(l_obj.Key), TESTING_IRRIGATION_ZONE_KEY_0_0)
        self.assertEqual(str(l_obj.Active), TESTING_IRRIGATION_ZONE_ACTIVE_0_0)
        self.assertEqual(str(l_obj.Comment), TESTING_IRRIGATION_ZONE_COMMENT_0_0)
        self.assertEqual(str(l_obj.Duration), TESTING_IRRIGATION_ZONE_DURATION_0_0)
        self.assertEqual(str(l_obj.EmitterCount), TESTING_IRRIGATION_ZONE_EMITTER_COUNT_0_0)
        self.assertEqual(str(l_obj.EmitterType), TESTING_IRRIGATION_ZONE_EMITTER_TYPE_0_0)
        self.assertEqual(str(l_obj.Next), TESTING_IRRIGATION_ZONE_NEXT_0_0)
        self.assertEqual(str(l_obj.Previous), TESTING_IRRIGATION_ZONE_PREV_0_0)
        self.assertEqual(str(l_obj.Rate), TESTING_IRRIGATION_ZONE_RATE_0_0)
        self.assertEqual(str(l_obj.StartTime), TESTING_IRRIGATION_ZONE_START_TIME_0_0)

    def test_02_System(self):
        """
        """
        l_xml = self.m_xml.irrigation_system
        l_obj = self.m_api._read_one_irrigation_system(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - System'))
        self.assertEqual(l_obj.Name, TESTING_IRRIGATION_SYSTEM_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_IRRIGATION_SYSTEM_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_IRRIGATION_SYSTEM_ACTIVE_0)
        self.assertEqual(str(l_obj.Comment), TESTING_IRRIGATION_SYSTEM_COMMENT_0)
        self.assertEqual(str(l_obj.FirstZone), TESTING_IRRIGATION_SYSTEM_FIRST_ZONE_0)
        self.assertEqual(str(l_obj.UsesMasterValve), TESTING_IRRIGATION_SYSTEM_MASTER_VALVE_0)
        self.assertEqual(str(l_obj.UsesPumpStartRelay), TESTING_IRRIGATION_SYSTEM_PUMP_RELAY_0)
        self.assertEqual(str(l_obj.Type), TESTING_IRRIGATION_SYSTEM_TYPE_0)

    def test_03_Irrigation(self):
        """
        """
        _l_xml = self.m_xml.irrigation_sect
        l_obj = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - Irrigation'))
        self.assertEqual(len(l_obj), 3)
        self.assertEqual(l_obj[0].Name, TESTING_IRRIGATION_SYSTEM_NAME_0)
        self.assertEqual(str(l_obj[0].Key), TESTING_IRRIGATION_SYSTEM_KEY_0)
        self.assertEqual(str(l_obj[0].Active), TESTING_IRRIGATION_SYSTEM_ACTIVE_0)
        self.assertEqual(l_obj[1].Name, TESTING_IRRIGATION_SYSTEM_NAME_1)
        self.assertEqual(str(l_obj[1].Key), TESTING_IRRIGATION_SYSTEM_KEY_1)
        self.assertEqual(str(l_obj[1].Active), TESTING_IRRIGATION_SYSTEM_ACTIVE_1)
        self.assertEqual(l_obj[2].Name, TESTING_IRRIGATION_SYSTEM_NAME_2)
        self.assertEqual(str(l_obj[2].Key), TESTING_IRRIGATION_SYSTEM_KEY_2)
        self.assertEqual(str(l_obj[2].Active), TESTING_IRRIGATION_SYSTEM_ACTIVE_2)


class W1_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Zone(self):
        """
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_sys = l_irr[0]
        l_obj = l_sys.Zones[0]
        l_xml = self.m_api._write_one_zone(l_obj)
        # print(PrettyFormatAny.form(l_obj, 'C1-01-A - Zone'))
        # print(PrettyFormatAny.form(l_xml, 'C1-01-B - Zone'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_IRRIGATION_ZONE_NAME_0_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_IRRIGATION_ZONE_KEY_0_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_IRRIGATION_ZONE_ACTIVE_0_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_IRRIGATION_ZONE_COMMENT_0_0)
        self.assertEqual(l_xml.find('Duration').text, TESTING_IRRIGATION_ZONE_DURATION_0_0)
        self.assertEqual(l_xml.find('EmitterCount').text, TESTING_IRRIGATION_ZONE_EMITTER_COUNT_0_0)
        self.assertEqual(l_xml.find('EmitterType').text, TESTING_IRRIGATION_ZONE_EMITTER_TYPE_0_0)
        self.assertEqual(l_xml.find('NextZone').text, TESTING_IRRIGATION_ZONE_NEXT_0_0)
        self.assertEqual(l_xml.find('PrevZone').text, TESTING_IRRIGATION_ZONE_PREV_0_0)
        self.assertEqual(l_xml.find('Rate').text, TESTING_IRRIGATION_ZONE_RATE_0_0)
        self.assertEqual(l_xml.find('StartTime').text, TESTING_IRRIGATION_ZONE_START_TIME_0_0)

    def test_02_System(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_sys = l_irr[0]
        l_xml = self.m_api._write_one_system(l_sys)
        # print(PrettyFormatAny.form(l_xml, 'C1-02-A - System'))
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, {})

    def test_03_Irrigation(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_obj = self.m_api.write_irrigation_xml(l_irr)
        # print(PrettyFormatAny.form(l_obj, 'C1-03-A - Irrigate'))
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, {})

# ## END DBK
