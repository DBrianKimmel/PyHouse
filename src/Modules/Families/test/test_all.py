"""
@name:      PyHouse/src/Modules/Families/test/test_all.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 28, 2015
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest, reporter, runner

from Modules.Families import test as I_test
from Modules.Utilities.tools import PrettyPrintAny


class Z_All(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_AllFamilies(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_all ***\n{}\n'.format(l_ret))

# ## END DBK
