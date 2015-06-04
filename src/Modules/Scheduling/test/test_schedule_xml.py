"""
@name:      PyHouse/src/Modules/Scheduling/test/test_schedule_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@Copyright: (c)  2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 2, 2014
@Summary:

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleBaseData
from Modules.Scheduling import schedule_xml
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_schedule_obj = ScheduleBaseData()
        self.m_api = schedule_xml.ReadWriteConfigXml()


class C01_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_xml.root, 'XML')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_xml.schedule_sect.tag, 'ScheduleSection', 'XML - No Schedules section')
        self.assertEqual(self.m_xml.schedule.tag, 'Schedule', 'XML - No Schedule section')
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'XML')
        PrettyPrintAny(self.m_xml.schedule_sect, 'Schedule')


class C02_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneBase(self):
        """ Read in the xml file and fill in x
        """
        l_schedule_obj = self.m_api._read_one_base_schedule(self.m_xml.schedule)
        PrettyPrintAny(l_schedule_obj)
        self.assertEqual(l_schedule_obj.Name, 'Evening 1')
        self.assertEqual(l_schedule_obj.Key, 0, 'No Key')
        self.assertEqual(l_schedule_obj.Mode, 0, 'No Mode')
        self.assertEqual(l_schedule_obj.Mode, 0, 'No Mode')

    def test_02_OneLight(self):
        # l_schedule_obj = self.m_api._read_one_base_schedule(self.m_xml.schedule)
        l_light = self.m_api._read_one_lighting_schedule(self.m_xml.schedule)
        PrettyPrintAny(l_light, 'Light part of schedule')
        self.assertEqual(l_light.LightName, 'lr_cans')
        self.assertEqual(l_light.Rate, 0)
        self.assertEqual(l_light.RoomName, 'Living Room')

    def test_03_OneSchedule(self):
        l_sched = self.m_api._read_one_schedule(self.m_xml.schedule)
        PrettyPrintAny(l_sched, 'Full Light Sched.')
        self.assertEqual(l_sched.Name, 'Evening 1')
        self.assertEqual(l_sched.LightName, 'lr_cans')
        self.assertEqual(l_sched.RoomName, 'Living Room')

    def test_04_AllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_schedules, 'All Schedules')
        PrettyPrintAny(l_schedules[1], 'Schedule 1')
        self.assertEqual(len(l_schedules), 4)


class C03_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneBase(self):
        l_schedule = self.m_api._read_one_schedule(self.m_xml.schedule)
        l_xml = self.m_api._write_one_base_schedule(l_schedule)
        PrettyPrintAny(l_xml, 'Base Schedule XML')

    def test_02_OneLight(self):
        l_schedule = self.m_api._read_one_schedule(self.m_xml.schedule)
        l_xml = self.m_api._write_one_base_schedule(l_schedule)
        self.m_api._write_one_light_schedule(l_schedule, l_xml)
        PrettyPrintAny(l_xml, 'Light schedule XML')

    def test_03_OneSchedule(self):
        l_schedule = self.m_api._read_one_schedule(self.m_xml.schedule)
        l_xml = self.m_api._write_one_schedule(l_schedule)
        PrettyPrintAny(l_xml, 'One Schedule XML')

    def test_04_AllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_schedules_xml(l_schedules)
        PrettyPrintAny(l_xml, 'All Schedules XML')

# ## END DBK
