"""
@name:      Modules/House/Entertainment/Samsung/_test/test_samsung.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 14, 2016
@summary:

Passed all 15 tests - DBK - 2020-01-28

"""

__updated__ = '2020-01-28'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Entertainment.Samsung.samsung import Api as samsungApi, LocalConfig as samsungConfig
# from Modules.Core.Utilities import convert
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Samsung:
    Name: Samsung Tv
    Comment: The LivingRoom TV set
    Device:
        - Name: Samsung
          Comment: Main Receiver
          Host:
              Name: samsung-01-pp
              IPv4: 172.16.9.1
              Port: 55000
          Type: TV
          Model: Unknown
"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_config = samsungConfig(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_x', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_samsung')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = samsungApi(self.m_pyhouse_obj)

    def test_01_Pyhouse(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertIsNotNone(self.m_pyhouse_obj)

    def test_02_House(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-02-A - House'))
        self.assertIsNotNone(self.m_pyhouse_obj.House)

    def test_03_Entertainment(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'A1-03-A - Entertainment'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Entertainment)

    def test_04_Samsung(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment['Samsung'], 'A1-04-A - Samsung'))
        self.assertIsNone(self.m_pyhouse_obj.House.Entertainment['Samsung'])


class C1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_pyhouse_obj.House.Entertainment = {}

    def test_01_Device(self):
        """ Read the xml and fill in the first room's dict
        """
        l_config = self.m_test_config['Samsung']['Device']
        print('C1-01-A - {}'.format(l_config))
        l_obj = self.m_config._extract_one_device(l_config)
        print(PrettyFormatAny.form(l_obj, 'C1-01-B - Device'))
        self.assertEqual(l_obj.Name, 'Samsung')

    def test_02_AllDevices(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = self.m_config._extract_all_devices(self.m_test_config['Samsung'])
        print(PrettyFormatAny.form(l_obj, 'C1-02-A - All Devices'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C1-02-B - All Devices'))

    def test_03_AllSamsung(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = self.m_config._extract_all_samsung(self.m_test_config, None)
        print(PrettyFormatAny.form(l_obj, 'C1-03-A - All Samsung'))


class D1_Write(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_pyhouse_obj.House.Entertainment = {}

    def test_01_Setup(self):
        """ Read the xml and fill in the first room's dict
        """
        pass
        # print(PrettyFormatAny.form(self.m_section, 'D1-01-A - Section'))
        # print(PrettyFormatAny.form(self.m_section.Devices[0], 'D1-01-B - One Device'))

    def test_02_OneDevice(self):
        """ Read the xml and fill in the first room's dict
        """
        l_xml = samsungXml._write_device(self.m_section.Devices[0])
        # print(PrettyFormatAny.form(l_xml, 'D1-02-A - One Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_SAMSUNG_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_SAMSUNG_DEVICE_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_SAMSUNG_DEVICE_COMMENT_0)

    def test_03_AllDevices(self):
        """
        """
        l_xml = samsungXml.write_samsung_section_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'D1-03-A - XML'))
        self.assertEqual(l_xml.find('Device').attrib['Name'], TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(l_xml.find('Device').attrib['Key'], TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(l_xml.find('Device').attrib['Active'], TESTING_SAMSUNG_DEVICE_ACTIVE_0)

# ## END DBK
