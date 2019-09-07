"""
@name:      Modules/Core/_test/test_Drivers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep  7, 2019
@Summary:

"""

__updated__ = '2019-09-07'

from twisted.trial import unittest, reporter, runner

from Modules.Core.Drivers import _test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Mqtt(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter(realtime=True)
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Drivers ***\n{}\n'.format(l_ret))

# ## END DBK
