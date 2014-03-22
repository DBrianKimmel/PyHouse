"""
Created on Mar 20, 2014

@author: briank
"""

from src.core import nodes
from src.core.pyhouse_data import PyHouseData

from twisted.trial import unittest


class Test(unittest.TestCase):

    def setUp(self):
        print("setUp")
        # self.m_api = nodes.API()
        # self.m_pyhouse_obj = PyHouseData()

    def tearDown(self):
        print("tearDown")
        pass

    def Xtest_001_Init(self):
        print("Test 001")
        l_api = nodes.API()
        self.assertIsNotNone(l_api)

    def test_002_StartServer(self):
        print("Test 002")
        l_api = nodes.API()
        l_pyhouse_obj = PyHouseData()
        l_api.StartServer(l_pyhouse_obj)

    def Xtest_003_StartClient(self):
        print("Test 003")
        l_api = nodes.API()
        l_pyhouse_obj = PyHouseData()
        l_api.StartClient(l_pyhouse_obj)


# if __name__ == '__main__':
#    unittest.main(verbosity = 2)

    # ## END DBK
