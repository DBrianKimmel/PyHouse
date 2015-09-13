"""
@name:      PyHouse/src/Modules/Scheduling/test/test_auto_update.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@note:      Created on Dec 31, 2013
@license:   MIT License
@summary:   Handle the automatic updating of PyHouse

Passed all 4 tests - DBK - 2015-09-12

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Scheduling import auto_update
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C00_Base(SetupMixin, unittest.TestCase):
    """ This section tests the basic setup code.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_00_Setup(self):
        """
        Test to be sure that setup is running OK.
        This test is repeated throughout the entire testing suite.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer division')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House division')


class C02_Local(SetupMixin, unittest.TestCase):
    """
    Test the local version getting code.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_01_PyHouse(self):
        l_file = auto_update.FindLocalVersion()._find_pyhouse_version_file()
        print('Local File = {0:}'.format(l_file))

    def test_02_Version(self):
        l_version = auto_update.FindLocalVersion().get_version()
        print(l_version)


class C03_Repository(SetupMixin, unittest.TestCase):
    """
    Test the repository version code
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_01_Version(self):
        l_version = auto_update.FindRepositoryVersion().get_version()
        print(l_version)

# ## END DBK
