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
from Modules.Core.data_objects import PyHousesData, HouseData, LocationData
from Modules.scheduling import schedule
from Modules.utils.tools import PrettyPrintObject, PrettyPrintXML, PrettyPrintDict, PrintObject
from Modules.utils import xml_tools
from src.test import xml_data

XML = xml_data.XML_LONG


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(XML)
        self.m_util = xml_tools.PutGetXML()
        self.m_api = schedule.API()

    def test_0101_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_find_houses(self):
        l_houses = self.m_root_element.find('Houses')
        self.assertEqual(l_houses.tag, 'Houses')

    def test_0103_xml_find_house(self):
        l_houses = self.m_root_element.find('Houses')
        l_list = l_houses.findall('House')
        for l_house in l_list:
            print("House {0:}".format(l_house.get('Name')))


class Test_02_ReadWriteXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def _pyHouses(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.HouseData = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root_xml = ET.fromstring(XML)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_schedules_xml = self.m_house_xml.find('Schedules')
        self.m_schedule_xml = self.m_schedules_xml.find('Schedule')
        self.m_house_obj = LocationData()
        self.m_api = schedule.API()

    def setUp(self):
        self._pyHouses()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouses_obj.HouseData.Rooms, {}, 'No Rooms{}')

    def test_0202_find_xml(self):
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
        PrettyPrintObject(l_schedule_obj)

    def test_0232_ReadAllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_schedules_xml)
        print(type(l_schedules))
        PrettyPrintDict(l_schedules)
        for k, v in l_schedules.iteritems():
            PrettyPrintObject(v)

    def test_0241_WriteOneSchedule(self):
        l_schedule = self.m_api.read_one_schedule_xml(self.m_schedule_xml)
        l_xml = self.m_api.write_one_schedule_xml(l_schedule)
        PrettyPrintXML(l_xml)

    def test_0242_WriteAllSchedules(self):
        l_schedules = self.m_api.read_schedules_xml(self.m_schedules_xml)
        l_xml = self.m_api.write_schedules_xml(l_schedules)
        PrettyPrintXML(l_xml)


class Test_03_Startup(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.HouseData = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root_xml = ET.fromstring(XML)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_schedules_xml = self.m_house_xml.find('Schedules')
        self.m_schedule_xml = self.m_schedules_xml.find('Schedule')
        self.m_house_obj = LocationData()
        self.m_api = schedule.API()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
            self.m_api.Start(self.m_pyhouses_obj)


# ## END
