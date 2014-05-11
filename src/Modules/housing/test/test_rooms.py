"""
@name: PyHouse/src/housing/test/test_rooms.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Test handling the rooms information for a house.
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.housing import rooms
from Modules.utils import xml_tools
from test import xml_data
from Modules.Core.data_objects import PyHouseData, HousesData, HouseData, RoomData

XML = xml_data.XML


class Test_02_XML(unittest.TestCase):

    def _pyHouses(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house = self.m_houses.find('House')
        self.m_house_obj = RoomData()

    def setUp(self):
        self._pyHouses()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouses_obj.HousesData[0].HouseObject.Rooms, {}, 'No Rooms{}')

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house.tag, 'House', 'XML - No House section')

    def test_0203_ReadXml(self):
        """ Read in the xml file and fill in the rooms dict
        """
        self.m_api = rooms.ReadWriteConfig()
        self.m_api.read_xml(self.m_pyhouses_obj.HousesData[0].HouseObject, self.m_house)

# ## END DBK
