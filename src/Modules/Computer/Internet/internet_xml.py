"""
-*- test-case-name: PyHouse.src.Modules.Computer.Internet.test.test_internet_xml -*-

@name: PyHouse/src/Modules/Computer/Internet/internet_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Sep 29, 2014
@Summary:

"""
# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import InternetConnectionData
from Modules.Utilities.xml_tools import XmlConfigTools
from Modules.Computer import logging_pyh as Logger

g_debug = 1
LOG = Logger.getLogger('PyHouse.Internet_xml   ')




class Util(XmlConfigTools):
    """
    This section is fairly well tested by the unit test module.
    """

    m_count = 0

    def _read_locates_xml(self, p_locater_sect_xml):
        l_dict = {}
        self.m_count = 0
        try:
            for l_xml in p_locater_sect_xml.iterfind('LocateUrl'):
                l_url = str(l_xml.text)
                l_dict[self.m_count] = l_url
                self.m_count += 1
        except AttributeError as e_err:
            print('ERROR in read_locates_xml - {}'.format(e_err))
        return l_dict

    def _read_updates_xml(self, p_updater_sect_xml):
        l_dict = {}
        self.m_count = 0
        try:
            for l_xml in p_updater_sect_xml.iterfind('UpdateUrl'):
                l_url = str(l_xml.text)
                l_dict[self.m_count] = l_url
                self.m_count += 1
        except AttributeError as e_err:
            print('ERROR in read_updates_xml - {}'.format(e_err))
        return l_dict

    def _read_derived(self, p_internet_sect_xml):
        l_icd = InternetConnectionData()
        try:
            l_icd.ExternalIPv4 = self.get_ip_from_xml(p_internet_sect_xml, 'ExternalIPv4')
            l_icd.ExternalIPv6 = self.get_ip_from_xml(p_internet_sect_xml, 'ExternalIPv6')
            l_icd.LastChanged = self.get_date_time_from_xml(p_internet_sect_xml, 'LastChanged')
        except:
            pass
        return l_icd


    def _write_locates_xml(self, p_internet_obj):
        l_xml = ET.Element('LocaterUrlSection')
        for l_url in p_internet_obj.LocateUrls.itervalues():
            self.put_text_element(l_xml, 'LocateUrl', l_url)
        return l_xml

    def _write_updates_xml(self, p_dns_obj):
        l_xml = ET.Element('UpdaterUrlSection')
        for l_url in p_dns_obj.UpdateUrls.itervalues():
            self.put_text_element(l_xml, 'UpdateUrl', l_url)
        return l_xml

    def _write_derived_xml(self, p_internet_obj, p_xml):
        self.put_text_element(p_xml, 'ExternalIPv4', p_internet_obj.ExternalIPv4)
        self.put_text_element(p_xml, 'ExternalIPv6', p_internet_obj.ExternalIPv6)
        self.put_text_element(p_xml, 'LastChanged', p_internet_obj.LastChanged)



class API(Util):

    def read_internet_xml(self, p_pyhouse_obj):
        """Reads zero or more <Internet> entries within the <InternetSection>
        @param p_internet_section_xml: is the <InternetSection> element
        """
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_xml = l_xml.find('ComputerDivision')
            l_internet_sect_xml = l_xml.find('InternetSection')
        except AttributeError as e_err:
            l_internet_sect_xml = None
            LOG.error('Internet section missing from XML - {}'.format(e_err))
        try:
            l_icd = self._read_derived(l_internet_sect_xml)
            l_icd.LocateUrls = self._read_locates_xml(l_internet_sect_xml.find('LocaterUrlSection'))
            l_icd.UpdateUrls = self._read_updates_xml(l_internet_sect_xml.find('UpdaterUrlSection'))
        except AttributeError as e_err:
            LOG.error('ERROR ReadInternet - {}'.format(e_err))
        LOG.info('Loaded Internet XML')
        return l_icd


    def write_internet_xml(self, p_internet_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @param p_internet_obj: is pyhouse_obj.Computer.InternetConnection
        @return: a sub tree ready to be appended to tree
        """
        l_xml = ET.Element('InternetSection')
        self._write_derived_xml(p_internet_obj, l_xml)
        l_xml.append(self._write_locates_xml(p_internet_obj))
        l_xml.append(self._write_updates_xml(p_internet_obj))
        return l_xml

# ## END DBK
