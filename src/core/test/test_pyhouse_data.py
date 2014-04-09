"""
PyHouse/src/core/test.test_pyhouse_data.py

Created on Mar 22, 2014


@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module is used to test a single module.
"""

from twisted.trial import unittest

import src.core.data_objects
from src.core import data_objects

class Test(unittest.TestCase):


    def setUp(self):
        print('Setup')


    def tearDown(self):
        print('Teardown')


    def test_001_Load(self):
        print('Test 001')
        _l_data = data_objects.PyHouseData()

    def test_002_houses(self):
        l_data = data_objects.PyHouseData()
        _l_houses = l_data.HousesData

    def test_003_house(self):
        l_data = data_objects.PyHouseData()
        l_houses = l_data.HousesData
        _l_house = l_houses.HouseObject[0]

    def test_004_name(self):
        l_data = data_objects.PyHouseData()
        l_houses = l_data.HousesData
        l_house = l_houses.HouseObject[0]
        l_name = l_house.Name
        self.assertEqual(l_name, 'Test House #1')
        print(l_name)

    def test_005_street(self):
        l_data = data_objects.PyHouseData()
        l_houses = l_data.HousesData
        l_house = l_houses.HouseObject[0]
        l_location = l_house.Location
        l_street = l_location.Street
        self.assertEqual(l_street, '5191 N Pink Poppy Dr')
        print(l_street)

# ## END DBK
