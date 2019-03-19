"""
@name:      PyHouse/src/Modules/Scheduling/test/test_auto_update.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2018 by D. Brian Kimmel
@note:      Created on Dec 31, 2013
@license:   MIT License
@summary:   Handle the automatic updating of PyHouse

Passed all 5 tests - DBK - 2015-11-21

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2019-03-18'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.test import proto_helpers
# import twisted.internet.test.reactormixins.ReactorBuilder

# Import PyMh files and modules.
from Modules.Housing.Scheduling import auto_update
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_transport = proto_helpers.StringTransport()


class A0(unittest.TestCase):
    """ Test all different set ups
    """

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_auto_update')


class B1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the basic setup code.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_01_PyHouse(self):
        l_file = auto_update._find_pyhouse_version_file()
        # print('B1-01-A - Local File = {}'.format(l_file))


class B2_Base(SetupMixin, unittest.TestCase):
    """ This section tests the basic setup code.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_01_Setup(self):
        """
        Test to be sure that setup is running OK.
        This test is repeated throughout the entire testing suite.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer division')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House division')


class C1_Local(SetupMixin, unittest.TestCase):
    """
    Test the local version getting code.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_01_FileName(self):
        """ Test finding the version file
        """
        l_file = auto_update.FindLocalVersion().get_filename()
        print('C1-01-A - Local File = {}'.format(l_file))

    def test_02_Version(self):
        """ Test extraction of the version number
        """
        l_file = auto_update.FindLocalVersion().get_filename()
        l_version = auto_update.FindLocalVersion().get_version(l_file)
        print('C1-02-A - Version = {}'.format(l_version))


class D1_Repository(SetupMixin, unittest.TestCase):
    """
    Test the repository version getting code
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_00_(self):
        """ Test finding the repository version file
        """
        print('\nD1-00-A - Remote\n')

    def test_01_Uri(self):
        """ Test finding the repository version file
        """
        l_uri = auto_update.FindRepositoryVersion(self.m_pyhouse_obj).get_uri()
        print('D1-01-A - Uri = {}\n'.format(l_uri))

    def test_02_Repository(self):
        """ Test extraction of the repository version number
        """
        l_repos = auto_update.FindRepositoryVersion(self.m_pyhouse_obj).get_repository()
        # print(PrettyFormatAny.form(l_repos, 'D1-02-A -  repo', 190), '\n')

    def test_03_File(self):
        """ Test extraction of the repository version number
        """
        l_file = auto_update.FindRepositoryVersion(self.m_pyhouse_obj).get_file()
        # print('D1-03-A -  {}'.format(l_file), '\n')
        print(PrettyFormatAny.form(l_file, 'D1-03-B -  file', 190), '\n')

    def test_04_Version(self):
        """ Test extraction of the repository version number
        """
        l_version = auto_update.FindRepositoryVersion(self.m_pyhouse_obj).get_version()
        print('D1-04-A -  {}'.format(l_version), '\n')


class E1_Download(SetupMixin, unittest.TestCase):
    """ Test fetching the repository and downloading it
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)


class F1_Restart(SetupMixin, unittest.TestCase):
    """ Test starting up PyHouse again.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

# ## END DBK
