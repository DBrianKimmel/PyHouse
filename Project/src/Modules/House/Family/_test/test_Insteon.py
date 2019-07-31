"""
@name:      PyHouse/src/Modules/Families/test/test_Insteon.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 16, 2014
@Summary:

passed all tests - DBK - 2018-02-13

"""

__updated__ = '2018-02-13'

# Import system type stuff
from twisted.trial import unittest, reporter, runner

from Modules.Families.Insteon import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Insteon(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Insteon ***\n{}\n'.format(l_ret))

# ## END DBK
