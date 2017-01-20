"""
@name:      PyHouse/src/Modules/Computer/Internet/test/test_internet_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 29, 2014
@Summary:

Passed all 16 tests - DBK - 2016-11-27

"""

__updated__ = '2017-01-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import datetime

# Import PyMh files
from Modules.Core.data_objects import InternetConnectionData
from Modules.Computer.Internet.internet_xml import API as internetAPI, Util as internetUtil
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import convert, json_tools
from Modules.Computer.Internet.test.xml_internet import \
    TESTING_INTERNET_LOCATE_URL_0_0, \
    TESTING_INTERNET_LOCATE_URL_0_1, \
    TESTING_INTERNET_UPDATE_URL_0_0, \
    TESTING_INTERNET_UPDATE_URL_0_1, \
    TESTING_INTERNET_IPv4_0, \
    TESTING_INTERNET_IPv6_0, \
    TESTING_INTERNET_UPDATE_INTERVAL_0, \
    TESTING_INTERNET_LAST_CHANGED_0, \
    TESTING_INTERNET_NAME_0, \
    TESTING_INTERNET_KEY_0, \
    TESTING_INTERNET_ACTIVE_0
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

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


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_internet_xml')


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        self.m_api = internetAPI()

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

    def test_02_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-1-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.internet_sect.tag, 'InternetSection')
        self.assertEqual(self.m_xml.internet_locater_sect.tag, 'LocateUrlSection')
        self.assertEqual(self.m_xml.internet_updater_sect.tag, 'UpdateUrlSection')

    def test_03_XML(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml.internet_sect, 'A1-03-A - XML'))
        pass



class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        self.m_api = internetAPI()

    def test_01_Derived(self):
        l_obj = internetUtil._read_derived(self.m_xml.internet)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - Addresses'))
        self.assertEqual(l_obj.Name, TESTING_INTERNET_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_INTERNET_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_INTERNET_ACTIVE_0)
        self.assertEqual(l_obj.ExternalIPv4, convert.str_to_long(TESTING_INTERNET_IPv4_0))
        self.assertEqual(l_obj.ExternalIPv6, convert.str_to_long(TESTING_INTERNET_IPv6_0))
        self.assertEqual(str(l_obj.LastChanged), TESTING_INTERNET_LAST_CHANGED_0)
        self.assertEqual(l_obj.UpdateInterval, TESTING_INTERNET_UPDATE_INTERVAL_0)

    def test_02_Locates(self):
        l_list = internetUtil._read_locates_xml(self.m_xml.internet)
        # print(PrettyFormatAny.form(l_list, 'B1-01-A - Locate URLs'))
        self.assertEqual(len(l_list), 2)
        self.assertEqual(l_list[0], TESTING_INTERNET_LOCATE_URL_0_0)
        self.assertEqual(l_list[1], TESTING_INTERNET_LOCATE_URL_0_1)

    def test_03_Updates(self):
        l_list = internetUtil._read_updates_xml(self.m_xml.internet)
        # print(PrettyFormatAny.form(l_list, 'B1-02-A - Update URLs'))
        self.assertEqual(len(l_list), 2)
        self.assertEqual(l_list[0], TESTING_INTERNET_UPDATE_URL_0_0)
        self.assertEqual(l_list[1], TESTING_INTERNET_UPDATE_URL_0_1)

    def test_04_One(self):
        l_obj = internetUtil._read_one_internet(self.m_xml.internet)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - Addresses'))
        self.assertEqual(l_obj.Name, TESTING_INTERNET_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_INTERNET_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_INTERNET_ACTIVE_0)
        self.assertEqual(l_obj.ExternalIPv4, convert.str_to_long(TESTING_INTERNET_IPv4_0))
        self.assertEqual(l_obj.ExternalIPv6, convert.str_to_long(TESTING_INTERNET_IPv6_0))
        self.assertEqual(str(l_obj.LastChanged), TESTING_INTERNET_LAST_CHANGED_0)
        self.assertEqual(l_obj.UpdateInterval, TESTING_INTERNET_UPDATE_INTERVAL_0)

    def test_05_AllInternet(self):
        l_obj = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-04-A - Internet'))
        self.assertEqual(len(l_obj), 2)
        self.assertEqual(l_obj[0].LocateUrls[0], TESTING_INTERNET_LOCATE_URL_0_0)
        self.assertEqual(l_obj[0].LocateUrls[1], TESTING_INTERNET_LOCATE_URL_0_1)
        self.assertEqual(l_obj[0].UpdateUrls[0], TESTING_INTERNET_UPDATE_URL_0_0)
        self.assertEqual(l_obj[0].UpdateUrls[1], TESTING_INTERNET_UPDATE_URL_0_1)
        self.assertEqual(l_obj[0].ExternalIPv4, convert.str_to_long(TESTING_INTERNET_IPv4_0))


class C1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        self.m_api = internetAPI()
        self.m_internet_dict = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.InternetConnection = self.m_internet_dict

    def test_01_Dict(self):
        """ Write out the XML file for the location section
        """
        # print(PrettyFormatAny.form(self.m_internet_dict, 'C1-01-A - Dict'))
        self.assertEqual(len(self.m_internet_dict), 2)

    def test_02_Derived(self):
        """ Write out the XML file for the location section
        """
        l_xml = internetUtil._write_derived_xml(self.m_internet_dict[0])
        # print(PrettyFormatAny.form(l_xml, 'C1-02-A - Locate'))
        self.assertEqual(l_xml.find('ExternalIPv4').text, TESTING_INTERNET_IPv4_0)
        self.assertEqual(l_xml.find('ExternalIPv6').text, TESTING_INTERNET_IPv6_0)
        self.assertEqual(l_xml._children[2].text, str(DATETIME))

    def test_03_Locates(self):
        l_xml = internetUtil._write_locates_xml(self.m_internet_dict[0])
        # print(PrettyFormatAny.form(l_xml, 'C1-03-A - Locate'))
        self.assertEqual(l_xml._children[0].text, TESTING_INTERNET_LOCATE_URL_0_0)

    def test_04_Updates(self):
        l_xml = internetUtil._write_updates_xml(self.m_internet_dict[0])
        # print(PrettyFormatAny.form(l_xml, 'C1-04-A - Locate'))
        self.assertEqual(l_xml._children[0].text, TESTING_INTERNET_UPDATE_URL_0_0)

    def test_05_One(self):
        """ Write out the XML file for the location section
        """
        # print(PrettyFormatAny.form(self.m_internet_dict, 'C1-04-A - Locate'))
        self.m_pyhouse_obj.Computer.InternetConnection = self.m_internet_dict
        l_xml = internetUtil._write_one_internet(self.m_internet_dict[0])
        # print(PrettyFormatAny.form(l_xml, 'C1-05-A - Locate'))
        self.assertEqual(l_xml.find('ExternalIPv6').text, TESTING_INTERNET_IPv6_0)

    def test_06_All(self):
        """ Write out the XML file for the location section
        """
        l_xml = internetAPI().write_internet_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'C1-06-A - Locate'))
        self.assertEqual(l_xml.find('Internet/ExternalIPv6').text, TESTING_INTERNET_IPv6_0)


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
        _l_json = json_tools.encode_json(l_internet)
        # print(PrettyFormatAny.form(l_json, 'JSON', 70))
        # self.assertEqual(self.jsonPair(l_json, 'ExternalIPv4'), convert.str_to_long(TESTING_INTERNET_IPv4_0))
        # self.assertEqual(self.jsonPair(l_json, 'ExternalIPv6'), convert.str_to_long(TESTING_INTERNET_IPv6_0))

# ## END DBK
