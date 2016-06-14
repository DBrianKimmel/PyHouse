"""
@name:      PyHouse/src/Modules/Scheduling/test/test_schedule_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 2, 2014
@Summary:

Passed all 9 tests - DBK - 2016-06-09

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleBaseData
from Modules.Scheduling.schedule_xml import Xml as scheduleXml
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Lighting.test.xml_lights import TESTING_LIGHT_NAME_0
from Modules.Scheduling.test.xml_schedule import TESTING_SCHEDULE_NAME_0, TESTING_SCHEDULE_KEY_0, \
    TESTING_SCHEDULE_MODE_0, TESTING_SCHEDULE_ACTIVE_0, TESTING_SCHEDULE_TYPE_0, TESTING_SCHEDULE_TIME_0, \
    TESTING_SCHEDULE_DOW_0, \
    TESTING_SCHEDULE_NAME_1, \
    TESTING_SCHEDULE_NAME_2, \
    TESTING_SCHEDULE_NAME_3, TESTING_SCHEDULE_DOW_1, \
    TESTING_SCHEDULE_DOW_2, TESTING_SCHEDULE_DOW_3
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_schedule_obj = ScheduleBaseData()
        self.m_api = scheduleXml()


class C01_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.schedule_sect.tag, 'ScheduleSection')
        self.assertEqual(self.m_xml.schedule.tag, 'Schedule')


class C02_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneBase(self):
        """ Read in the xml file and fill in x
        """
        l_schedule_obj = scheduleXml._read_one_base_schedule(self.m_xml.schedule)
        self.assertEqual(l_schedule_obj.Name, TESTING_SCHEDULE_NAME_0)
        self.assertEqual(l_schedule_obj.Key, int(TESTING_SCHEDULE_KEY_0))
        self.assertEqual(l_schedule_obj.Active, bool(TESTING_SCHEDULE_ACTIVE_0))
        self.assertEqual(l_schedule_obj.ScheduleType, TESTING_SCHEDULE_TYPE_0)
        self.assertEqual(l_schedule_obj.DOW, int(TESTING_SCHEDULE_DOW_0))
        self.assertEqual(l_schedule_obj.ScheduleMode, TESTING_SCHEDULE_MODE_0)
        self.assertEqual(l_schedule_obj.Time, TESTING_SCHEDULE_TIME_0)

    def test_02_OneLight(self):
        # l_schedule_obj = scheduleXml._read_one_base_schedule(self.m_xml.schedule)
        l_light = scheduleXml._read_one_lighting_schedule(self.m_xml.schedule)
        print(PrettyFormatAny.form(l_light, 'One Light'))
        self.assertEqual(l_light.LightName, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.Rate, 0)
        self.assertEqual(l_light.RoomName, 'Living Room')

    def test_03_OneSchedule(self):
        l_sched = scheduleXml._read_one_schedule(self.m_xml.schedule)
        print(PrettyFormatAny.form(l_sched, 'One Schedule'))
        self.assertEqual(l_sched.Name, 'Evening 1')
        self.assertEqual(l_sched.LightName, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_sched.RoomName, 'Living Room')

    def test_04_AllSchedules(self):
        l_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_schedules, 'Schedules'))
        print(PrettyFormatAny.form(l_schedules[0], 'Schedules'))
        self.assertEqual(len(l_schedules), 4)


class C03_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneBase(self):
        l_schedule = scheduleXml._read_one_schedule(self.m_xml.schedule)
        l_xml = scheduleXml._write_one_base_schedule(l_schedule)
        print(PrettyFormatAny.form(l_xml, 'One Interface'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_SCHEDULE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_SCHEDULE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_SCHEDULE_ACTIVE_0)
        self.assertEqual(l_xml[1].text, TESTING_SCHEDULE_DOW_0)
        self.assertEqual(l_xml[2].text, TESTING_SCHEDULE_MODE_0)
        self.assertEqual(l_xml[3].text, TESTING_SCHEDULE_TYPE_0)
        self.assertEqual(l_xml[4].text, TESTING_SCHEDULE_TIME_0)

    def test_02_OneLight(self):
        l_schedule = scheduleXml._read_one_schedule(self.m_xml.schedule)
        l_xml = scheduleXml._write_one_base_schedule(l_schedule)
        scheduleXml._write_one_light_schedule(l_schedule, l_xml)
        print(PrettyFormatAny.form(l_xml, 'One Interface'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_SCHEDULE_NAME_0)

    def test_03_OneSchedule(self):
        l_schedule = scheduleXml._read_one_schedule(self.m_xml.schedule)
        l_xml = scheduleXml._write_one_schedule(l_schedule)
        print(PrettyFormatAny.form(l_xml, 'One Interface'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_SCHEDULE_NAME_0)

    def test_04_AllSchedules(self):
        l_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        l_xml, l_count = scheduleXml.write_schedules_xml(l_schedules)
        print(PrettyFormatAny.form(l_xml, 'One Interface'))
        self.assertEqual(l_count, len(l_schedules))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_SCHEDULE_NAME_0)
        self.assertEqual(l_xml[0][1].text, TESTING_SCHEDULE_DOW_0)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_SCHEDULE_NAME_1)
        self.assertEqual(l_xml[1][1].text, TESTING_SCHEDULE_DOW_1)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_SCHEDULE_NAME_2)
        self.assertEqual(l_xml[2][1].text, TESTING_SCHEDULE_DOW_2)
        self.assertEqual(l_xml[3].attrib['Name'], TESTING_SCHEDULE_NAME_3)
        self.assertEqual(l_xml[3][1].text, TESTING_SCHEDULE_DOW_3)

# ## END DBK
