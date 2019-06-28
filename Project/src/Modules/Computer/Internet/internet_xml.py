"""
@name:      PyHouse/Project/src/Modules/Computer/Internet/internet_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 29, 2014
@Summary:

"""

__updated__ = '2019-06-19'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.data_objects import InternetConnectionData
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Internet_xml   ')


class Util(object):
    """
    This section is fairly well tested by the unit test module.
    """

    @staticmethod
    def _read_derived(p_xml):
        """
        @param p_xml: points to a single "Internet" element
        """
        l_obj = InternetConnectionData()
        try:
            l_obj.Name = PutGetXML.get_text_from_xml(p_xml, 'Name')
            l_obj.Key = PutGetXML.get_int_from_xml(p_xml, 'Key', 0)
            l_obj.Active = PutGetXML.get_bool_from_xml(p_xml, 'Active', False)
            l_obj.ExternalIPv4 = PutGetXML.get_ip_from_xml(p_xml, 'ExternalIPv4')
            l_obj.ExternalIPv6 = PutGetXML.get_ip_from_xml(p_xml, 'ExternalIPv6')
            l_obj.LastChanged = PutGetXML.get_date_time_from_xml(p_xml, 'LastChanged')
            l_obj.UpdateInterval = PutGetXML.get_text_from_xml(p_xml, 'UpdateInterval')
        except:
            pass
        return l_obj

    @staticmethod
    def _write_derived_xml(p_obj):
        l_xml = ET.Element('Internet')
        PutGetXML.put_text_attribute(l_xml, 'Name', p_obj.Name)
        PutGetXML.put_int_attribute(l_xml, 'Key', p_obj.Key)
        PutGetXML.put_bool_attribute(l_xml, 'Active', p_obj.Active)
        PutGetXML.put_ip_element(l_xml, 'ExternalIPv4', p_obj.ExternalIPv4)
        PutGetXML.put_ip_element(l_xml, 'ExternalIPv6', p_obj.ExternalIPv6)
        PutGetXML.put_date_time_element(l_xml, 'LastChanged', p_obj.LastChanged)
        PutGetXML.put_text_element(l_xml, 'UpdateInterval', p_obj.UpdateInterval)
        return l_xml

    @staticmethod
    def _read_locates_xml(p_xml):
        l_list = []
        l_count = 0
        l_xml = p_xml.find('LocateUrlSection')
        if l_xml == None:
            return l_list
        for l_xml in l_xml.iterfind('LocateUrl'):
            l_url = str(l_xml.text)
            l_list.append(l_url)
            l_count += 1
        return l_list

    @staticmethod
    def _write_locates_xml(p_obj):
        l_xml = ET.Element('LocaterUrlSection')
        l_urls = p_obj.LocateUrls
        for l_url in l_urls:
            PutGetXML.put_text_element(l_xml, 'LocateUrl', l_url)
        return l_xml

    @staticmethod
    def _read_updates_xml(p_xml):
        l_list = []
        l_count = 0
        l_xml = p_xml.find('UpdateUrlSection')
        if l_xml == None:
            return l_list
        for l_xml in l_xml.iterfind('UpdateUrl'):
            l_url = str(l_xml.text)
            l_list.append(l_url)
            l_count += 1
        return l_list

    @staticmethod
    def _write_updates_xml(p_obj):
        l_xml = ET.Element('UpdaterUrlSection')
        l_urls = p_obj.UpdateUrls
        for l_url in l_urls:
            PutGetXML.put_text_element(l_xml, 'UpdateUrl', l_url)
        return l_xml

    @staticmethod
    def _read_one_internet(p_xml):
        l_obj = Util._read_derived(p_xml)
        l_obj.LocateUrls = Util._read_locates_xml(p_xml)
        l_obj.UpdateUrls = Util._read_updates_xml(p_xml)
        return l_obj

    @staticmethod
    def _write_one_internet(p_obj):
        l_xml = Util._write_derived_xml(p_obj)
        l_xml.append(Util._write_locates_xml(p_obj))
        l_xml.append(Util._write_updates_xml(p_obj))
        return l_xml


class API(object):

    def read_internet_xml(self, p_pyhouse_obj):
        """Reads zero or more <Internet> entries within the <InternetSection>
        @param p_internet_section_xml: is the <InternetSection> element
        """
        l_dict = {}
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'ComputerDivision/InternetSection')
        if l_xml == None:
            return l_dict
        l_count = 0
        for l_internet in l_xml.iterfind('Internet'):
            l_obj = Util._read_one_internet(l_internet)
            l_dict[l_count] = l_obj
            l_count += 1
        LOG.info('Loaded {} Internet XML '.format(l_count))
        return l_dict

    def write_internet_xml(self, p_pyhouse_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @param p_internet_obj: is pyhouse_obj.Computer.InternetConnection
        @return: a sub tree ready to be appended to tree
        """
        l_ret = ET.Element('InternetSection')
        for l_obj in p_pyhouse_obj.Computer.InternetConnection.values():
            l_ret.append(Util._write_derived_xml(l_obj))
            l_ret.append(Util._write_locates_xml(l_obj))
            l_ret.append(Util._write_updates_xml(l_obj))
        return l_ret

#  ## END DBK
