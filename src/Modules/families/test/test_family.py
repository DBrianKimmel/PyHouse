"""
@name: PyHouse/Modules/families/test/test_family.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on May 17, 2013
@license: MIT License
@summary: This module is for testing family.
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HousesData, HouseData, RoomData
from Modules.families import family
from test import xml_data

XML = xml_data.XML


class Test_01_Families(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house = self.m_houses.find('House')
        self.m_house_obj = RoomData()
        self.m_api = family.API()

    def test_0101_ValidFamilies(self):
        self.assertEqual(family.VALID_FAMILIES[0], 'Insteon')

    def test_0102_build_one(self):
        l_ret = self.m_api.build_one_family('Insteon', 1)
        self.assertEqual(l_ret.Name, 'Insteon')

    def test_0103_import(self):
        l_family_obj = self.m_api.build_one_family('Insteon', 1)
        l_ret = self.m_api.import_module(l_family_obj)
        print('Return:{0:}'.format(l_ret))

# ## END DBK
