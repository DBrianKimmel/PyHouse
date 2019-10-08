"""
@name:      Modules/House/Family/Hue/_test/test_Hue_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 18, 2017
@summary:   Test

Passed all 2 tests - DBK - 2018-01-27

"""

__updated__ = '2019-10-08'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Family.hue.hue_config import HueInformation


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Hue_device')


class C01_Api(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = Insteon_device.Api(self.m_pyhouse_obj)
        self.m_device = HueInformation()

    def test_01_Init(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(Test_02_Api('test_0202_Init'))
    return suite

# ## END DBK
