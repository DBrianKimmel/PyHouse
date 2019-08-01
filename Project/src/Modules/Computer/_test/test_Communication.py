"""
@name:      PyHouse/src/Modules/_test/test_communication.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 16, 2014
@Summary:

"""

__updated__ = '2019-07-12'

# Import system type stuff
from twisted.trial import unittest, reporter, runner

# Import PyMh files and modules.
from Modules.Computer.Communication import test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Mqtt(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter(realtime=True)
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Communication ***\n{}\n'.format(l_ret))

# ## END DBK
