"""
@name: PyHouse/src/communication/test/test_ir_control.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 22, 2014
@summary: Test
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from src.communication import ir_control
from src.utils import xml_tools
from src.test import xml_data
from src.core.data_objects import PyHouseData, HousesData, HouseData, RoomData

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
        self.m_api = ir_control.API()

    def setUp(self):
        pass


    def tearDown(self):
        pass

# ## END DBK
