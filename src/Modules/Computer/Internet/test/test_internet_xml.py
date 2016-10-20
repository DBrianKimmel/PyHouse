"""
@name:      PyHouse/src/Modules/Computer/Internet/test/test_internet_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 29, 2014
@Summary:

Passed all 11 tests - DBK - 2015-09-12

"""

__updated__ = '2016-10-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import datetime

# Import PyMh files
from Modules.Core.data_objects import InternetConnectionData
from Modules.Computer.Internet.internet_xml import API as internetAPI, Util as internetUtil
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import convert, json_tools
from Modules.Computer.Internet.test.xml_internet import \
        TESTING_INTERNET_IPv6, \
        TESTING_INTERNET_LOCATE_URL_0, \
        TESTING_INTERNET_UPDATE_URL_0, \
        TESTING_INTERNET_IPv4, TESTING_INTERNET_LOCATE_URL_1, TESTING_INTERNET_UPDATE_URL_1
from Modules.Utilities.debug_tools import PrettyFormatAny

DATETIME = datetime.datetime(2014, 10, 2, 12, 34, 56)


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

    def jsonPair(self, p_json, p_key):
        """ Extract key, value from json
        """
        l_json = json_tools.decode_json_unicode(p_json)
        try:
            l_val = l_json[p_key]
        except KeyError as e_err:
            print('ERROR - {}'.format(e_err))
            l_val = 'ERRor {}'.format(e_err)
        return l_val


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        self.m_api = internetAPI()

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, None)

    def test_2_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-1-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.internet_sect.tag, 'InternetSection')
        self.assertEqual(self.m_xml.internet_locater_sect.tag, 'LocateUrlSection')
        self.assertEqual(self.m_xml.internet_updater_sect.tag, 'UpdateUrlSection')



class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        self.m_api = internetAPI()

    def test_01_ReadLocates(self):
        l_list = internetUtil._read_locates_xml(self.m_xml.internet_locater_sect)
        # print(PrettyFormatAny.form(l_list, 'B1-01-A - Locate URLs'))
        self.assertEqual(len(l_list), 2)
        self.assertEqual(l_list[0], TESTING_INTERNET_LOCATE_URL_0)
        self.assertEqual(l_list[1], TESTING_INTERNET_LOCATE_URL_1)

    def test_02_ReadUpdates(self):
        l_list = internetUtil._read_updates_xml(self.m_xml.internet_updater_sect)
        # print(PrettyFormatAny.form(l_list, 'B1-02-A - Update URLs'))
        self.assertEqual(len(l_list), 2)
        self.assertEqual(l_list[0], TESTING_INTERNET_UPDATE_URL_0)
        self.assertEqual(l_list[1], TESTING_INTERNET_UPDATE_URL_1)

    def test_03_ReadDerived(self):
        l_icd = internetUtil._read_derived(self.m_xml.internet_sect)
        # print(PrettyFormatAny.form(l_icd, 'B1-03-A - Addresses'))
        self.assertEqual(l_icd.ExternalIPv4, convert.str_to_long(TESTING_INTERNET_IPv4))
        self.assertEqual(l_icd.ExternalIPv6, convert.str_to_long(TESTING_INTERNET_IPv6))
        self.assertEqual(l_icd.LastChanged, DATETIME)

    def test_04_RedAllInternet(self):
        l_obj = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'B1-04-A - Internet'))
        self.assertEqual(l_obj.LocateUrls[0], TESTING_INTERNET_LOCATE_URL_0)
        self.assertEqual(l_obj.LocateUrls[1], TESTING_INTERNET_LOCATE_URL_1)
        self.assertEqual(l_obj.UpdateUrls[0], TESTING_INTERNET_UPDATE_URL_0)
        self.assertEqual(l_obj.UpdateUrls[1], TESTING_INTERNET_UPDATE_URL_1)
        self.assertEqual(l_obj.ExternalIPv4, convert.str_to_long(TESTING_INTERNET_IPv4))


class C1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        self.m_api = internetAPI()

    def test_01_WriteLocates(self):
        l_obj = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        l_xml = internetUtil._write_locates_xml(l_obj)
        print(PrettyFormatAny.form(l_xml, 'C1-01-A - Locate'))
        self.assertEqual(l_xml._children[0].text, TESTING_INTERNET_LOCATE_URL_0)

    def test_02_WriteUpdates(self):
        l_internet_obj = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        l_xml = internetUtil._write_updates_xml(l_internet_obj)
        print(PrettyFormatAny.form(l_xml, 'C1-01-A - Locate'))
        self.assertEqual(l_xml._children[0].text, TESTING_INTERNET_UPDATE_URL_0)

    def test_03_WriteDerived(self):
        """ Write out the XML file for the location section
        """
        l_internet = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_internet, 'C1-01-A - Locate'))
        l_xml = ET.Element('InternetSection')
        internetUtil._write_derived_xml(l_internet, l_xml)
        print(PrettyFormatAny.form(l_xml, 'C1-01-B - Locate'))
        self.assertEqual(l_xml.find('ExternalIPv4').text, TESTING_INTERNET_IPv4)
        self.assertEqual(l_xml.find('ExternalIPv6').text, TESTING_INTERNET_IPv6)
        self.assertEqual(l_xml._children[2].text, str(DATETIME))

    def test_04_WriteAllInternetXml(self):
        """ Write out the XML file for the location section
        """
        l_internet = internetAPI().read_internet_xml(self.m_pyhouse_obj)
        l_xml = internetAPI().write_internet_xml(l_internet)
        print(PrettyFormatAny.form(l_xml, 'C1-01-A - Locate'))
        self.assertEqual(l_xml.find('ExternalIPv6').text, TESTING_INTERNET_IPv6)


class D1_JSON(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        self.m_api = internetAPI()

    def test_01_Create(self):
        """ Create a JSON object for Internets.
        """
        l_internet = internetAPI().read_internet_xml(self.m_pyhouse_obj)
        l_json = json_tools.encode_json(l_internet)
        # print(PrettyFormatAny.form(l_json, 'JSON', 70))
        self.assertEqual(self.jsonPair(l_json, 'ExternalIPv4'), convert.str_to_long(TESTING_INTERNET_IPv4))
        self.assertEqual(self.jsonPair(l_json, 'ExternalIPv6'), convert.str_to_long(TESTING_INTERNET_IPv6))

# ## END DBK
