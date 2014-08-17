"""
@name: PyHouse/src/Modules/Families/Insteon/test/test_Insteon.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Aug 16, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest, reporter

# Import PyMh files and modules.
from Modules.Families.Insteon.test import test_Insteon_decoder, test_Insteon_device, test_Insteon_PLM, \
        test_Insteon_utils, test_Insteon_xml


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_Insteon_decoder.suite())
    test_suite.addTest(test_Insteon_device.suite())
    test_suite.addTest(test_Insteon_PLM.suite())
    test_suite.addTest(test_Insteon_utils.suite())
    test_suite.addTest(test_Insteon_xml.suite())
    return test_suite


class Test_99_Family(unittest.TestCase):
    """
    """

    m_test = suite()

    def setUp(self):
        print('Setup')
        pass

    def test_9999_Insteon(self):
        print(self.m_test)
        l_ret = reporter.TestResult()
        self.m_test.run(l_ret)
        l_ret.done()
        print('9999 Insteon')

# ## END DBK
