"""
@name: PyHouse/src/Modules/housing/test/test_house.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the schedule information for a house.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleData
from Modules.scheduling import schedule
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

        self.m_schedule_obj = ScheduleData()
        self.m_api = schedule.API()


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
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'Schedules')

    def test_0231_ReadOneSchedule(self):
        """ Read in the xml file and fill in x
        """
        l_schedule_obj = self.m_api.read_one_schedule_xml(self.m_xml.schedule)
        self.assertEqual(l_schedule_obj.Name, 'Evening')
        PrettyPrintAny(l_schedule_obj)

    def test_0239_ReadAllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_schedules, 'All Schedules A')
        for _k, v in l_schedules.iteritems():
            PrettyPrintAny(v, 'All Schedules B')

    def test_0241_WriteOneSchedule(self):
        l_schedule = self.m_api.read_one_schedule_xml(self.m_xml.schedule)
        l_xml = self.m_api.write_one_schedule_xml(l_schedule)
        PrettyPrintAny(l_xml)

    def test_0242_WriteAllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_schedules_xml(l_schedules)
        PrettyPrintAny(l_xml)


class Test_03_Execution(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.OBJs.Schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)

    def test_0301_GetNext(self):
        l_delay, l_list = self.m_api.get_next_sched(self.m_pyhouse_obj)
        print('Delaying {0:} Seconds'.format(l_delay))
        PrettyPrintAny(l_list, 'Schedule List')

    def test_0303_RunSchedule(self):
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'Schedules')

    def test_0305_SchedulesList(self):
        pass

    def test_0307_OneSchedule(self):
        pass
        self.m_api.execute_one_schedule(3)

    def test_0309_DispatchSchedule(self):
        pass

class Test_04_Utility(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.OBJs.Schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)

    def test_0401_SubstituteTime(self):
        self.m_api._substitute_time(p_timefield)
        pass

    def test_0455_Next(self):
        self.m_api.get_next_sched()

# ## END
