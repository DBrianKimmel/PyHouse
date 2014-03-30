"""
Created on Mar 2, 2014

@author: briank
"""

from src.core import setup
from src.core.pyhouse_data import PyHouseData

from twisted.trial import unittest
from twisted.internet.defer import Deferred, gatherResults, maybeDeferred
from twisted.internet import protocol, error, defer, udp
from twisted.python import runtime


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test(self):
        pass

    def _test_errors(self):
        pass

    def test_001_errors(self):
        print("Test 001")
        self._test_errors()

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
