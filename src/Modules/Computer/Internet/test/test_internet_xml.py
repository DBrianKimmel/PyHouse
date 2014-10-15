"""
@name: PyHouse/src/Modules/Computer/Internet/test/test_internet_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Sep 29, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
import datetime
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import InternetConnectionData
from Modules.Computer.Internet import internet_xml
from Modules.Web import web_utils
from Modules.Utilities.tools import PrettyPrintAny
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import convert


DATETIME = datetime.datetime(2014, 10, 2, 12, 34, 56)



class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C01_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        self.m_api = internet_xml.API()

    def test_00_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        PrettyPrintAny(self.m_xml.root.tag)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer section')
        self.assertEqual(self.m_xml.internet_sect.tag, 'InternetSection', 'XML - No Internet section')
        self.assertEqual(self.m_xml.locater_sect.tag, 'LocaterUrlSection')
        self.assertEqual(self.m_xml.updater_sect.tag, 'UpdaterUrlSection')
        PrettyPrintAny(self.m_xml.internet_sect, 'All Internet Section')
        PrettyPrintAny(self.m_xml.locater_sect)

    def test_01_ReadLocates(self):
        l_dict = self.m_api._read_locates_xml(self.m_xml.locater_sect)
        PrettyPrintAny(l_dict, 'Locates')
        self.assertEqual(len(l_dict), 2)
        self.assertEqual(l_dict[0], 'http://snar.co/ip/')

    def test_02_ReadUpdates(self):
        l_dict = self.m_api._read_updates_xml(self.m_xml.updater_sect)
        self.assertEqual(len(l_dict), 1)
        self.assertEqual(l_dict[0], 'http://freedns.afraid.org/dynamic/update.php?abc')
        PrettyPrintAny(l_dict, 'Updates')

    def test_03_ReadDerived(self):
        l_icd = self.m_api._read_derived(self.m_xml.internet_sect)
        PrettyPrintAny(l_icd, 'ICD')
        self.assertEqual(l_icd.ExternalIPv4, convert.str_to_long('65.35.48.61'))
        self.assertEqual(l_icd.ExternalIPv6, convert.str_to_long('1234:5678::1'))
        self.assertEqual(l_icd.LastChanged, DATETIME)

    def test_04_RedAllInternet(self):
        l_obj = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_obj, 'All Internet')
        self.assertEqual(l_obj.LocateUrls[0], 'http://snar.co/ip/')
        self.assertEqual(l_obj.UpdateUrls[0], 'http://freedns.afraid.org/dynamic/update.php?abc')
        self.assertEqual(l_obj.ExternalIPv4, convert.str_to_long('65.35.48.61'))

    def test_11_WriteLocates(self):
        l_internet_obj = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        l_xml = self.m_api._write_locates_xml(l_internet_obj)
        PrettyPrintAny(l_xml, 'Locates')
        self.assertEqual(l_internet_obj.LocateUrls[0], 'http://snar.co/ip/')

    def test_12_WriteUpdates(self):
        l_internet_obj = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        l_xml = self.m_api._write_updates_xml(l_internet_obj)
        PrettyPrintAny(l_xml, 'Updatew')

    def test_13_WriteDerived(self):
        """ Write out the XML file for the location section
        """
        l_internet = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        l_xml = ET.Element('InternetSection')
        self.m_api._write_derived_xml(l_internet, l_xml)
        PrettyPrintAny(l_xml, 'Write xml')

    def test_14_WriteAllInternetXml(self):
        """ Write out the XML file for the location section
        """
        l_internet = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_internet, 'Internet', 100)
        l_xml = self.m_api.write_internet_xml(l_internet)
        PrettyPrintAny(l_xml, 'Write xml')

    def test_20_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        l_internet = self.m_api.read_internet_xml(self.m_pyhouse_obj)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_internet))
        PrettyPrintAny(l_json, 'JSON', 70)


# ## END DBK
