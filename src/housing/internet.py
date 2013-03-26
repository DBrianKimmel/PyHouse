#!/usr/bin/env python

"""Get the internet address and make reports available for web interface.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET
from twisted.internet import reactor
from twisted.web.client import getPage

from utils import xml_tools


g_debug = 9
g_logger = None

IP_HOST = 'http://snar.co/ip'
DNS_HOST = 'http://freedns.afraid.org/dynamic/update.php?VDZtSkE2MzFVMVVBQVd5QXg2MDo5MjU1MzYw'

callLater = reactor.callLater

class InternetData(object):

    def __init__(self):
        self.DynDns = {}

class DynDnsData(object):

    def __init__(self):
        self.Active = False
        self.Interval = None
        self.Key = 0
        self.Name = ''
        self.Url = 15 * 60


class ReadWriteXML(xml_tools.ConfigTools):
    """
    <House>
        <internet>
            <DynamicDNS>
    """

    def extract_dyn_dns(self, p_internet_obj, p_internet_xml):
        self.read_common(p_internet_obj, p_internet_xml)
        p_internet_obj.Interval = self.get_int(p_internet_xml, 'Interval')
        p_internet_obj.Url = self.get_text(p_internet_xml, 'Url')
        if g_debug >= 6:
            print "internet.extract_dyn_dns() - Name:{0:}, Interval:{1:}, Url:{2:};".format(p_internet_obj.Name, p_internet_obj.Interval, p_internet_obj.Url)
        return p_internet_obj

    def insert_dyn_dns(self):
        pass

    def read_internet(self, p_house_obj, p_house_xml):
        """
        """
        if g_debug >= 4:
            print "internet.read_internet()"
        l_dict = {}
        l_sect = p_house_xml.find('Internet')
        try:
            l_list = l_sect.iterfind('DynamicDNS')
        except AttributeError:
            l_list = []
        for l_entry in l_list:
            self.extract_dyn_dns(p_house_obj, l_entry)
        p_house_obj.Internet = l_dict
        return l_dict

    def write_internet(self, p_internet_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to "something"
        """
        if g_debug >= 4:
            print "internet.write_internet()"
        l_internet_xml = ET.Element('Internet')
        try:
            for l_dyndns_obj in p_internet_obj.itervalues():
                l_entry = self.xml_create_common_element('DynamicDNS', l_dyndns_obj)
                ET.SubElement(l_entry, 'Interval').text = str(l_dyndns_obj.Interval)
                ET.SubElement(l_entry, 'Url').text = str(l_dyndns_obj.Url)
        except AttributeError:
            pass
        return l_internet_xml


class DynDnsAPI(object):

    def __init__(self, p_house_obj):
        self.m_house_obj = p_house_obj
        self.get_public_ip(IP_HOST)

    def get_public_ip(self, p_url):
        if g_debug >= 2:
            print "internet.get_public_ip()"
        l_ip_page = getPage(p_url)
        l_ip_page.addCallback(self.parse_ip_page)

    def parse_ip_page(self, p_ip_page):
        if g_debug >= 2:
            print "internet.parse_ip_page()", p_ip_page
        pass


class API(ReadWriteXML):

    m_house_obj = None

    def __init__(self, p_house_obj):
        global g_logger
        g_logger = logging.getLogger('PyHouse.Internet')
        if g_debug >= 1:
            print "internet.API.__init__()"
        g_logger.info("Initializing for house:{0:}.".format(p_house_obj.Name))
        self.m_house_obj = p_house_obj
        g_logger.info("Initialized.")

    def Start(self, p_house_obj, p_house_xml):
        self.m_house_obj = p_house_obj
        if g_debug >= 1:
            print "internet.API.Start() for house:{0:}".format(p_house_obj.Name)
        g_logger.info("Starting for house:{0:}.".format(self.m_house_obj.Name))
        self.read_internet(self.m_house_obj, p_house_xml)
        DynDnsAPI(self.m_house_obj)
        g_logger.info("Started.")

    def Stop(self):
        if g_debug >= 1:
            print "internet.API.Stop() - 1"
        g_logger.info("Stopping for house:{0:}.".format(self.m_house_obj.Name))
        l_internet_xml = self.write_internet(self.m_house_obj.Internet)
        if g_debug >= 1:
            print "internet.API.Stop() - 2 "
        g_logger.info("Stopped.")
        return l_internet_xml

# ## END
