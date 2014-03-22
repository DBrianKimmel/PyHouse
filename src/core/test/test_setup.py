"""
Created on Mar 2, 2014

@author: briank
"""

from src.core import setup
from src.core.pyhouse_data import PyHouseData

from twisted.trial import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_Init(self):
        print("Test 001")
        _m_api = setup.API()

    def test_002_PyHouses(self):
        print("Test 002")
        _m_api = setup.API()
        _m_pyhouse_obj = PyHouseData()

    def test_003_Start(self):
        print("Test 003")
        m_api = setup.API()
        m_pyhouse_obj = PyHouseData()
        m_api.Start(m_pyhouse_obj)

# ## END DBK
