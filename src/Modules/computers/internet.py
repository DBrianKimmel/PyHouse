"""
-*- test-case-name: PyHouse.src.Modules.Comps.test.test_internet -*-

@Name: PyHouse/src/Modules/Comps/internet.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 20, 2012
@summary: This module determines the IP address of the ISP connection.


Get the internet address and make reports available for web interface.

Since PyHouse is always running (as a daemon) this module will get the IP-v4 address that is
assigned to our router by the ISP.
It will then take that IP address and update our Dynamic DNS provider(s) so we may browse to that
address from some external device and check on the status of the house.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import InternetConnectionData, InternetConnectionDynDnsData
from Modules.computers import inet_find_snar, inet_update_freedns
from Modules.utils.xml_tools import XmlConfigTools
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Internet    ')


class ReadWriteConfigXml(XmlConfigTools):
    """
    This section is fairly well tested by the unit test module.
    """

    m_count = 0
    m_count_d = 0

    def read_one_dyn_dns_xml(self, p_dyn_dns_xml):
        """Reads a single <DynamicDns Name=...> element
        """
        l_dyndns_obj = InternetConnectionDynDnsData()
        self.read_base_object_xml(l_dyndns_obj, p_dyn_dns_xml)
        l_dyndns_obj.UpdateInterval = self.get_int_from_xml(p_dyn_dns_xml, 'UpdateInterval')
        l_dyndns_obj.UpdateUrl = self.get_text_from_xml(p_dyn_dns_xml, 'UpdateUrl')
        return l_dyndns_obj

    def read_dyn_dns_xml(self, p_dns_sect_element):
        """Reads a <DynamicDnsSection> wich has zero or more <DynmicDns Name=....> elements
        """
        self.m_count_d = 0
        l_ret = {}
        for l_entry_xml in p_dns_sect_element.iterfind('DynamicDNS'):
            l_dyndns = self.read_one_dyn_dns_xml(l_entry_xml)
            l_dyndns.Key = self.m_count_d  # Renumber
            l_ret[self.m_count_d] = l_dyndns
            self.m_count_d += 1
        return l_ret

    def read_one_internet_xml(self, p_internet_element):
        """Read one <Internet> element.
        Most computers will have only one but allow for more.
        May have a <DynamicDnsSection> contained.

        @param p_internet_element: a <Internet Name...> element
        @return: a internetConnectionData object
        """
        l_internet_obj = InternetConnectionData()
        self.read_base_object_xml(l_internet_obj, p_internet_element)
        l_internet_obj.Key = self.m_count  # Renumber
        try:
            l_internet_obj.ExternalIPv4 = self.get_text_from_xml(p_internet_element, 'ExternalIP')
            l_internet_obj.ExternalDelay = self.get_int_from_xml(p_internet_element, 'ExternalDelay')
            l_internet_obj.ExternalUrl = self.get_text_from_xml(p_internet_element, 'ExternalUrl')
        except AttributeError:
            LOG.error('internet section missing - using defaults.')
            l_internet_obj.ExternalDelay = 600
        l_internet_obj.DynDns = self.read_dyn_dns_xml(p_internet_element.find('DynamicDnsSection'))
        LOG.info('Loaded UpdateUrl:{0:}, Delay:{1:}'.format(l_internet_obj.ExternalUrl, l_internet_obj.ExternalDelay))
        return l_internet_obj

    def read_internet_xml(self, p_internet_section_xml):
        """Reads zero or more <Internet> entries within the <InternetSection>
        @param p_internet_section_xml: is the <InternetSection> element
        """
        l_ret = {}
        try:
            l_list = p_internet_section_xml.iterfind('Internet')
            for l_entry in l_list:
                # PrettyPrintAny(l_entry, 'Internet - read_internet_xml - InternetSectionEntry')
                l_inet = self.read_one_internet_xml(l_entry)
                l_inet.Key = self.m_count  # Renumber
                l_ret[self.m_count] = l_inet
                self.m_count += 1
        except AttributeError:
            pass
        return l_ret


    def write_one_dyn_dns_xml(self, p_dyn_dns_obj):
        l_entry = self.write_base_object_xml('DynmicDns', p_dyn_dns_obj)
        self.put_text_element(l_entry, 'UpdateUrl', p_dyn_dns_obj.UpdateUrl)
        self.put_int_element(l_entry, 'UpdateInterval', p_dyn_dns_obj.UpdateInterval)
        return l_entry

    def write_dyn_dns_xml(self, p_dns_obj):
        l_xml = ET.Element('DynamicDnsSection')
        self.m_count_d = 0
        for l_dns in p_dns_obj.itervalues():
            l_entry = self.write_one_dyn_dns_xml(l_dns)
            l_xml.append(l_entry)
            self.m_count_d += 1
        return l_xml

    def write_one_internet_xml(self, p_internet_obj):
        l_entry = self.write_base_object_xml('Internet', p_internet_obj)
        self.put_text_element(l_entry, 'ExternalIP', p_internet_obj.ExternalIPv4)
        self.put_int_element(l_entry, 'ExternalDelay', p_internet_obj.ExternalDelay)
        self.put_text_element(l_entry, 'ExternalUrl', p_internet_obj.ExternalUrl)
        l_entry.append(self.write_dyn_dns_xml(p_internet_obj.DynDns))
        return l_entry

    def write_internet_xml(self, p_internet_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @param p_internet_obj: is pyhouse_obj.Computer.InternetConnection
        @return: a sub tree ready to be appended to tree
        """
        l_xml = ET.Element('InternetSection')
        self.m_count = 0
        for l_internet_obj in p_internet_obj.itervalues():
            l_entry = self.write_one_internet_xml(l_internet_obj)
            l_xml.append(l_entry)
            self.m_count += 1
        return l_xml


class Utility(ReadWriteConfigXml):
    """
    """

    def find_xml(self, p_pyhouse_obj):
        """ Find the XML InternetSection.

        @return: the XML element <InternetSection>
        """
        l_ret = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_ret = l_ret.find('ComputerDivision')
            l_ret = l_ret.find('InternetSection')
        except AttributeError:
            pass
        return l_ret

    def start_internet_discovery(self, p_pyhouse_obj):
        for l_ix in self.m_pyhouse_obj.Computer.InternetConnection.iterkeys():
            inet_find_snar.API().Start(p_pyhouse_obj, l_ix)
            inet_update_freedns.API().Start(p_pyhouse_obj, l_ix)

    def stop_internet_discovery(self, p_pyhouse_obj):
        for l_ix in self.m_pyhouse_obj.Computer.InternetConnection.iterkeys():
            inet_find_snar.API().Stop(p_pyhouse_obj, l_ix)
            inet_update_freedns.API().Stop(p_pyhouse_obj, l_ix)


class API(Utility):

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        """
        Start async operation of the internet module.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pyhouse_obj.Computer.InternetConnection = self.read_internet_xml(self.find_xml(p_pyhouse_obj))
        self.start_internet_discovery(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        """
        Stop async operations.
        """
        self.stop_internet_discovery(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        p_xml.append(self.write_internet_xml(self.m_pyhouse_obj.Computer.InternetConnection))
        LOG.info('Saved XML')


# ## END DBK
