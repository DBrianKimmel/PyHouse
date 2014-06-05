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
from Modules.Core.data_objects import PyHouseData, HouseData, RoomData
from Modules.communication import ir_control
from src.test import xml_data

XML = xml_data.XML_LONG


class Test_02_XML(unittest.TestCase):

    def _pyHouses(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house = self.m_houses.find('House')
        self.m_house_obj = RoomData()
        self.m_api = ir_control.API()

    def setUp(self):
        pass


    def tearDown(self):
        pass

# ## END DBK
