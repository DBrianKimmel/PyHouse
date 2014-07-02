"""
@name: PyHouse/src/computer/test/test_internet.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the internet information for a computer.

XML tests all run OK - DBK 2014-07-01
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import InternetConnectionData, InternetConnectionDynDnsData
from Modules.Comps import internet
from Modules.web import web_utils
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data, test_mixin


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

        self.m_computer_div_xml = self.m_root_xml.find('ComputerDivision')
        self.m_internet_sect_xml = self.m_computer_div_xml.find('InternetSection')
        self.m_internet_xml = self.m_internet_sect_xml.find('Internet')
        self.m_dns_sect_xml = self.m_internet_xml.find('DynamicDnsSection')
        self.m_dyn_dns_xml = self.m_dns_sect_xml.find('DynamicDNS')
        self.m_internet_obj = InternetConnectionData()
        self.m_dyn_dns_obj = InternetConnectionDynDnsData()
        self.m_api = internet.API()

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_computer_div_xml.tag, 'ComputerDivision', 'XML - No Computer section')
        self.assertEqual(self.m_internet_sect_xml.tag, 'InternetSection', 'XML - No Internet section')
        self.assertEqual(self.m_internet_xml.tag, 'Internet', 'XML - No Internet section')
        self.assertEqual(self.m_dyn_dns_xml.tag, 'DynamicDNS', 'XML - No Internet section')
        PrettyPrintAny(self.m_internet_sect_xml, 'All Internet Section', 120)

    def test_0211_read_one_dyn(self):
        l_obj = self.m_api.read_one_dyn_dns_xml(self.m_dyn_dns_xml)
        self.assertEqual(l_obj.Name, 'Afraid', 'Bad DynDns Name')
        PrettyPrintAny(l_obj, 'One DynDns', 100)

    def test_0212_read_all_dyn(self):
        l_obj = self.m_api.read_one_dyn_dns_xml(self.m_dns_sect_xml)
        PrettyPrintAny(l_obj, 'All DynDns')

    def test_0213_ReadOneInternet(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_obj = self.m_api.read_one_internet_xml(self.m_internet_xml)
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML file')
        self.assertEqual(self.m_internet_sect_xml.tag, 'InternetSection', 'XML - No Internet section')
        self.assertEqual(self.m_internet_xml.tag, 'Internet', 'XML - No Internet entry')
        PrettyPrintAny(l_obj, 'One Internet')

    def test_0214_RedAllInternet(self):
        l_obj = self.m_api.read_internet_xml(self.m_internet_sect_xml)
        PrettyPrintAny(l_obj, 'All Internet')
        PrettyPrintAny(l_obj[0], 'All Internet [0]')

    def test_0221_write_one_dyn(self):
        l_dyn_obj = self.m_api.read_one_dyn_dns_xml(self.m_dyn_dns_xml)
        l_xml = self.m_api.write_one_dyn_dns_xml(l_dyn_obj)
        PrettyPrintAny(l_xml, 'One DynDns')
        self.assertEqual(l_dyn_obj.Name, 'Afraid', 'Bad DynDns Name')

    def test_0222_write_all_dyn(self):
        l_dyn_obj = self.m_api.read_dyn_dns_xml(self.m_dns_sect_xml)
        l_xml = self.m_api.write_dyn_dns_xml(l_dyn_obj)
        PrettyPrintAny(l_xml, 'All DynDns')

    def test_0223_WriteOneInternetXml(self):
        """ Write out the XML file for the location section
        """
        l_internet = self.m_api.read_one_internet_xml(self.m_internet_xml)
        l_xml = self.m_api.write_one_internet_xml(l_internet)
        PrettyPrintAny(l_xml, 'Write xml')

    def test_0224_WriteAllInternetXml(self):
        """ Write out the XML file for the location section
        """
        l_internet = self.m_api.read_internet_xml(self.m_internet_sect_xml)
        PrettyPrintAny(l_internet, 'Internet', 100)
        l_xml = self.m_api.write_internet_xml(l_internet)
        PrettyPrintAny(l_xml, 'Write xml')

    def test_0231_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        l_internet = self.m_api.read_internet_xml(self.m_internet_sect_xml)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_internet))
        print('JSON: {0:}'.format(l_json))


# class Test_03_GetExternalIp(unittest.TestCase):


#    def setUp(self):
#        self.m_pyhouse_obj = PyHouseData()
#        self.m_api = internet.API()

#    def test_0301_createClient(self):
#        # l_client = self.m_api.Start(self.m_pyhouse_obj, self.m_house_obj, self.m_house_xml)
#        pass

# ## END DBK
