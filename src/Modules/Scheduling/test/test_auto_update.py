"""
Created on Mar 24, 2014

@author: briank
"""

from Modules.scheduling import auto_update

from twisted.trial import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_001_LocalVersion(self):
        l_version = auto_update.FindLocalVersion().get_version()
        print(l_version)

    def test_002_RepositoryVersion(self):
        l_version = auto_update.FindRepositoryVersion().get_version()
        print(l_version)

# ## END DBK
