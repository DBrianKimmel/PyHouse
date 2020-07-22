"""
@name:      Modules/Housing/_test/_test-Rules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2020 by D. Brian Kimmel
@note:      Created on Feb 13, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2019-12-30'

from twisted.trial import unittest, reporter, runner

from Modules.Housing.Rules import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Pool(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Rules ***\n{}\n'.format(l_ret))

# ## END DBK

# ## END DBK
