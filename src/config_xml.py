#!/usr/bin/env python

"""
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

import house
import xml_tools


House_Data = house.Location_Data

g_xmltree = ''

class ReadConfig(object):
    """
    """

    m_fh = None

    def __init__(self):
        global g_xmltree
        self.m_fh = xml_tools.open_config()
        g_xmltree = ET.parse(self.m_fh)


class WriteConfig(object):
    """Use the internal data to write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    m_filename = None
    m_root = None

    def __init__(self):
        global g_xmltree
        self.m_filename = xml_tools.open_config()
        g_xmltree = ET.parse(self.m_filename)
        self.m_root = g_xmltree.getroot()
        l_nice = xml_tools.prettify(self.m_root)
        print l_nice

    def write_file(self):
        l_fh = open(self.m_filename, 'w')
        g_xmltree.write(self.m_filename)

    def write_houses(self):
        """Replace the data in the 'Houses' section with the current data.
        """
        #for h in g_xmltree.findall('House'):
        #    self.m_root.remove(h)
        l_sect = self.m_root.find('Houses')
        l_sect.clear()
        for l_obj in House_Data.itervalues():
            print "XLM writing houses: {0:}".format(l_obj.Name)
            l_house = ET.SubElement(l_sect, 'House')
            l_house.set('Name', l_obj.Name)
            l_house.set('Key', str(l_obj.Key))
            l_strt = ET.SubElement(l_house, 'Street')
            l_strt.text = l_obj.Street
            l_city = ET.SubElement(l_house, 'City')
            l_city.text = l_obj.City
            l_stat = ET.SubElement(l_house, 'State')
            l_stat.text = l_obj.State
            l_zipc = ET.SubElement(l_house, 'ZipCode')
            l_zipc.text = l_obj.ZipCode
            l_phon = ET.SubElement(l_house, 'Phone')
            l_phon.text = l_obj.Phone
            l_latl = ET.SubElement(l_house, 'Latitude')
            l_latl.text = str(l_obj.Latitude)
            l_long = ET.SubElement(l_house, 'Longitude')
            l_long.text = str(l_obj.Longitude)
            l_actv = ET.SubElement(l_house, 'Active')
            l_actv.text = str(l_obj.Active)
            l_timz = ET.SubElement(l_house, 'TimeZone')
            l_timz.text = str(l_obj.TimeZone)
            l_svgt = ET.SubElement(l_house, 'SavingTime')
            l_svgt.text = str(l_obj.SavingTime)
        self.write_file()

### END
