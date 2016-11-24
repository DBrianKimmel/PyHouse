"""
@name:      PyHouse/src/Modules/test/test_Utilities.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 28, 2015
@Summary:

"""

__updated__ = '2016-11-22'

# Import system type stuff
from twisted.trial import unittest, reporter, runner

# Import PyMh files and modules.
from Modules.Utilities import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Utilities(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Utilities ***\n{}\n'.format(l_ret))

# ## END DBK
