"""
@name:      PyHouse/src/Modules/_test/test_Irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 31, 2015
@Summary:

"""

__updated__ = '2016-11-21'

from twisted.trial import unittest, reporter, runner

from Modules.Housing.Irrigation import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Irrigation(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Irrigation ***\n{}\n'.format(l_ret))

# ## END DBK
