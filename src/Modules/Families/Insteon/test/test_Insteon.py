"""
@name: PyHouse/src/Modules/Families/Insteon/test/test_Insteon.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Aug 16, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest, reporter, runner

# Import PyMh files and modules.
from Modules.Families.Insteon.test import \
        test_Insteon_decoder, test_Insteon_device, test_Insteon_PLM, \
        test_Insteon_utils, \
        test_Insteon_xml
from Modules.Families.Insteon import test as I_test
from Modules.Utilities.tools import PrettyPrintAny


class Test_99_Family(unittest.TestCase):
    """
    """

    def setUp(self):
        # print('Setup')
        self.m_test = runner.TestLoader()

    def test_9999_Insteon(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        # l_ret = reporter.TestResult()
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        print('9999 Insteon', l_ret)
        # print('  Errors: {0:}'.format(PrettyPrintAny(l_ret.errors, '')))
        l_ret.printErrors()

# ## END DBK
