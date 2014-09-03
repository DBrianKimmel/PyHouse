"""
@name: PyHouse/src/Modules/Scheduling/test/test_schedule.py
@author: D. Brian Kimmel
@contact: d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the schedule information for a house.

"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleBaseData
from Modules.Scheduling import schedule, schedule_xml
from Modules.Scheduling import sunrisesunset
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


class Test_03_Execution(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.OBJs.Schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        self.date_2013_06_06 = datetime.date(2013, 6, 6)
        self.m_ss_api = sunrisesunset.API().Start(self.m_pyhouse_obj, self.date_2013_06_06)

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
        self.m_timefield = 0

    def test_0401_SubstituteTime(self):
        self.m_api._substitute_time(self.m_timefield)

    def test_0455_Next(self):
        self.m_api.get_next_sched()

# ## END
