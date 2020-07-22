"""
@name:      Modules/Core/Drivers/_test/test_Usb.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 30, 2015
@Summary:

Passed all tests - DBK - 2019-01-10

"""

__updated__ = '2020-01-21'

# Import system type stuff
from twisted.trial import unittest, reporter, runner

# Import PyMh files and modules.
from Modules.Core.Drivers.Usb import _test as I_test


class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_USB(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_USB ***\n{}\n'.format(l_ret))

# ## END DBK
