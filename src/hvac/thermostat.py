'''
Created on Mar 27, 2013

@author: briank
'''

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools

g_debug = 9
g_logger = None


class ReadWriteXML(xml_tools.ConfigTools):
    """
    """

    def read_internet(self, p_house_obj, p_house_xml):
        """
        """
        if g_debug >= 4:
            print "internet.read_internet()"
        l_dict = {}
        l_sect = p_house_xml.find('xxyyzz')
        try:
            l_list = l_sect.iterfind('aabbcc')
        except AttributeError:
            l_list = []
        for l_entry in l_list:
            # self.extract_dyn_dns(p_house_obj, l_entry)
            pass
        # p_house_obj.Internet = l_dict
        return l_dict

    def write_internet(self, p_internet_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to "something"
        """
        if g_debug >= 4:
            print "internet.write_internet()"
        l_internet_xml = ET.Element('xxyyzz')
        try:
            for l_dyndns_obj in p_internet_obj.itervalues():
                l_entry = self.xml_create_common_element('aabbcc', l_dyndns_obj)
                # ET.SubElement(l_entry, 'Interval').text = str(l_dyndns_obj.Interval)
                # ET.SubElement(l_entry, 'Url').text = str(l_dyndns_obj.Url)
        except AttributeError:
            pass
        return l_internet_xml


class API(object):

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
