"""
@name:      PyHouse/src/Modules/_test/test_Security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 31, 2015
@Summary:

Passed all tests - DBK - 2018-02-13

"""

__updated__ = '2018-02-13'

from twisted.trial import unittest, reporter, runner

from Modules.Housing.Security import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Security(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Security ***\n{}\n'.format(l_ret))

# ## END DBK
