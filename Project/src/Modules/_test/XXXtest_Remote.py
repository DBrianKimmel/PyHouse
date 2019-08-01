"""
@name:      PyHouse/src/Modules/_test/test_Remote.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 31, 2015
@Summary:

"""

__updated__ = '2019-07-12'

from twisted.trial import unittest, reporter, runner

from Modules.Remote import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Remote(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Remote ***\n{}\n'.format(l_ret))

# ## END DBK
