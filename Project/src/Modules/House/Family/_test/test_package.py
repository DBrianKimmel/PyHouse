"""
@Name:      PyHouse/src/Modules/Family/_test/test_package.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 9, 2013
@summary:   This module

Passed all 6 tests - DBK 2018-02-13
"""

__updated__ = '2018-02-13'

# Import system type stuff
import inspect
import os
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families.__init__ import VALID_FAMILIES


class Test_01(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_0101_valid_families(self):
        _path_inspect = inspect.getfile(inspect.currentframe())  # script filename (usually with path)
        path_file = os.path.abspath(__file__)
        l_dir = os.path.dirname(path_file)
        l_dir = os.path.dirname(l_dir)
        l_dir_list = os.listdir(l_dir)
        for l_name in VALID_FAMILIES:
            self.assertTrue(l_name in l_dir_list)
            # print("found {}".format(l_name))
        # print(l_dir_list)
        # families = os.dirs

    def test_0109_allDefined(self):
        pass

    def test_0111_Insteon(self):
        l_name = 'Insteon._test'
        # unittest.TestSuite(l_name)
        # suite = unittest.TestLoader().loadTestsFromTestCase(test_Insteon_device().Test_02_API)
        pass


class Test_02_Insteon(unittest.TestCase):

    def setUp(self):
        # print('Test Insteon')
        pass

    def tearDown(self):
        pass

    def test_0101_ValidFamilies(self):
        _path_inspect = inspect.getfile(inspect.currentframe())  # script filename (usually with path)
        path_file = os.path.abspath(__file__)
        l_dir = os.path.dirname(path_file)
        l_dir = os.path.dirname(l_dir)
        l_dir_list = os.listdir(l_dir)
        for l_name in VALID_FAMILIES:
            self.assertTrue(l_name in l_dir_list)
            # print("found {}".format(l_name))

    def test_0109_allDefined(self):
        pass

    def test_0111_Insteon(self):
        l_name = 'Insteon._test'
        # unittest.TestSuite(l_name)
        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_02_Insteon('test_0101_ValidFamilies'))
    suite.addTest(Test_02_Insteon('test_allDefined'))
    return suite


class MySuite():
    """
    """

# ## END
