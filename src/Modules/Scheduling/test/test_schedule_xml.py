"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Scheduling/test/test_schedule_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Sep 2, 2014
@Summary:

"""


# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleBaseData
from Modules.Scheduling import schedule_xml
from test import xml_data
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


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_0201_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_xml.schedule_sect.tag, 'ScheduleSection', 'XML - No Schedules section')
        self.assertEqual(self.m_xml.schedule.tag, 'Schedule', 'XML - No Schedule section')
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'XML')

    def test_0231_ReadOneBase(self):
        """ Read in the xml file and fill in x
        """
        l_schedule_obj = self.m_api.read_one_base_schedule(self.m_xml.schedule)
        PrettyPrintAny(l_schedule_obj)
        self.assertEqual(l_schedule_obj.Name, 'Evening')
        self.assertEqual(l_schedule_obj.Key, 0, 'No Key')
        self.assertEqual(l_schedule_obj.Mode, 0, 'No Mode')

    def test_0232_ReadOneLight(self):
        # l_schedule_obj = self.m_api.read_one_base_schedule(self.m_xml.schedule)
        l_light = self.m_api.read_one_lighting_schedule(self.m_xml.schedule)
        PrettyPrintAny(l_light, 'Light part of schedule')
        self.assertEqual(l_light.LightName, 'lr_cans')

    def test_0238_ReadOneSchedule(self):
        l_schedule_obj = self.m_api.read_one_schedule(self.m_xml.schedule)
        PrettyPrintAny(l_schedule_obj, 'Full Light Sched.')

    def test_0239_ReadAllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_schedules, 'All Schedules')
        PrettyPrintAny(l_schedules[1], 'Schedule 1')

    def test_0241_WriteOneBase(self):
        l_schedule = self.m_api.read_one_schedule(self.m_xml.schedule)
        l_xml = self.m_api.write_one_base_schedule(l_schedule)
        PrettyPrintAny(l_xml, 'Base Schedule XML')

    def test_0242_WriteOneLight(self):
        l_schedule = self.m_api.read_one_schedule(self.m_xml.schedule)
        l_xml = self.m_api.write_one_base_schedule(l_schedule)
        l_xml2 = self.m_api.write_one_light_schedule(l_schedule, l_xml)
        PrettyPrintAny(l_xml2, 'Light schedule XML')

    def test_0248_WriteOneSchedule(self):
        l_schedule = self.m_api.read_one_schedule(self.m_xml.schedule)
        l_xml = self.m_api.write_one_schedule(l_schedule)
        PrettyPrintAny(l_xml, 'One Schedule XML')

    def test_0249_WriteAllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_schedules_xml(l_schedules)
        PrettyPrintAny(l_xml, 'All Schedules XML')

# ## END DBK
