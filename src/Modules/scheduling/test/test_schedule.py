"""
@name: PyHouse/src/Modules/housing/test/test_house.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the information for a house.

Created on Apr 8, 2013

@author: briank
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseData, LocationData
from Modules.scheduling import schedule
from Modules.utils.tools import PrettyPrintAny
from Modules.utils import xml_tools
from src.test import xml_data


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_api = schedule.API()

        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml

        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_schedules_xml = self.m_house_xml.find('Schedules')
        self.m_schedule_xml = self.m_schedules_xml.find('Schedule')
        # print('SetupMixin setUp ran')


class Test_02_ReadWriteXML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_schedules_xml.tag, 'Schedules', 'XML - No Schedules section')
        self.assertEqual(self.m_schedule_xml.tag, 'Schedule', 'XML - No Schedule section')

    def test_0231_ReadOneSchedule(self):
        """ Read in the xml file and fill in x
        """
        l_schedule_obj = self.m_api.read_one_schedule_xml(self.m_schedule_xml)
        self.assertEqual(l_schedule_obj.Name, 'Evening')
        PrettyPrintAny(l_schedule_obj)

    def test_0232_ReadAllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_schedules_xml)
        PrettyPrintAny(l_schedules, 'All Schedules')
        for _k, v in l_schedules.iteritems():
            PrettyPrintAny(v, 'All Schedules-2')

    def test_0241_WriteOneSchedule(self):
        l_schedule = self.m_api.read_one_schedule_xml(self.m_schedule_xml)
        l_xml = self.m_api.write_one_schedule_xml(l_schedule)
        PrettyPrintAny(l_xml)

    def test_0242_WriteAllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_schedules_xml)
        l_xml = self.m_api.write_schedules_xml(l_schedules)
        PrettyPrintAny(l_xml)


class Test_03_Execution(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)
        self.m_schedules = self.m_api.read_schedules_xml(self.m_schedules_xml)
        pass

    def test_0301_RunSchedule(self):
        pass

    def test_0302_SchedulesList(self):
        pass

    def test_0303_OneSchedule(self):
        self.m_api.execute_one_schedule(3)

    def test_0304_DispatchSchedule(self):
        pass


class Test_04_Utility(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)
        pass

    def test_0401_substitute(self):
        # l_schedules = self.m_api.read_schedules_xml(self.m_schedules_xml)
        # self.m_api._substitute_time(p_timefield)
        pass


class Test_05_API(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_schedules_xml = self.m_house_xml.find('Schedules')
        self.m_schedule_xml = self.m_schedules_xml.find('Schedule')
        self.m_house_obj = LocationData()
        self.m_api = schedule.API()

    def Xtest_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.m_api.Start(self.m_pyhouses_obj)


# ## END
