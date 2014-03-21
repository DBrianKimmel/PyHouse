"""
Created on Mar 2, 2014

@author: briank
"""

from src.core import setup
from src.core.pyhouse_data import PyHouseData

from twisted.trial import unittest


class Test(unittest.TestCase):

    def setUp(self):
        m_api = setup.API()
        m_pyhouse_obj = PyHouseData()
        m_api.Start(m_pyhouse_obj)

    def tearDown(self):
        pass

    def test_001Name(self):
        pass

# ## END DBK
