"""
@name: PyHouse/src/Modules/Core/test/test_pyhouse_data.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Mar 22, 2014
@license: MIT License
@summary: test ?.

"""

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core import data_objects

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

    def Xtest_003_house(self):
        l_data = data_objects.PyHouseData()

    def Xtest_004_name(self):
        l_data = data_objects.PyHouseData()
        l_house = l_data.HousesData
        l_name = l_house.Name
        self.assertEqual(l_name, 'Test House #1')
        print(l_name)

    def Xtest_005_street(self):
        l_data = data_objects.PyHouseData()
        l_house = l_data.HousesData
        l_location = l_house.Location
        l_street = l_location.Street
        self.assertEqual(l_street, '5191 N Pink Poppy Dr')
        print(l_street)

# ## END DBK
