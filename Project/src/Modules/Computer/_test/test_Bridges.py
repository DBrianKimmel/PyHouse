"""
-*- _test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/_test/test_Bridges.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/_test/test_Bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 21, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2018-02-12'

# Import system type stuff
from twisted.trial import unittest, reporter, runner

from Modules.Computer.Bridges import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Mqtt(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter(realtime=True)
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Bridges ***\n{}\n'.format(l_ret))

# ## END DBK
