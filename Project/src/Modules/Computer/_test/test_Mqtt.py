"""
@name:      PyHouse/src/Modules/Computer/_test/test_Mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 29, 2015
@Summary:

"""

__updated__ = '2019-07-06'

from twisted.trial import unittest, reporter, runner

from Modules.Core.Mqtt import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Mqtt(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter(realtime=True)
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Mqtt ***\n{}\n'.format(l_ret))

# ## END DBK
