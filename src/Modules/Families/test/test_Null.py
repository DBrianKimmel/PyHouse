"""
@name:      PyHouse/src/Modules/Families/test/test_Null.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 28, 2015
@Summary:

Passed all tests - DBK - 2018-02-13
"""

__updated__ = '2018-02-13'

# Import system type stuff
from twisted.trial import unittest, reporter, runner

# Import PyMh files and modules.
from Modules.Families.Null import test as I_test


class Z_Null(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Null(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Null ***\n{}\n'.format(l_ret))

# ## END DBK
