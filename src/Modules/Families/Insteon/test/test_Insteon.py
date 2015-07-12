"""
@name:      PyHouse/src/Modules/Families/Insteon/test/test_Insteon.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 16, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest, reporter, runner

# Import PyMh files and modules.
# from Modules.Families.Insteon.test import \
#        test_Insteon_decoder, test_Insteon_device, test_Insteon_PLM, \
#        test_Insteon_utils, \
#        test_Insteon_xml
from Modules.Families.Insteon import test as I_test


class C99_Family(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_9999_Insteon(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        print('9999 Insteon', l_ret)
        l_ret.printErrors()

# ## END DBK
