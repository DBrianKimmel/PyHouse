"""
@name:      PyHouse/src/Modules/Computer/test/test_Internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 29, 2015
@Summary:

"""

__updated__ = '2016-11-22'


# Import system type stuff
from twisted.trial import unittest, reporter, runner

from Modules.Computer.Internet import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Internet(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        l_ret.printErrors()
        #
        print('\n====================\n*** test_Internet ***\n{}\n'.format(l_ret))

# ## END DBK
