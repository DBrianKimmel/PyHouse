#!/usr/bin/env python

"""
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

import house
import lighting
import schedule
import xml_tools


House_Data = house.Location_Data
Light_Data = lighting.Light_Data
Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data
Schedule_Data = schedule.Schedule_Data

g_xmltree = ''

class ReadConfig(object):
    """
    """

    m_fh = None

    def __init__(self):
        print "ReadConfig XML"
        global g_xmltree
        self.m_fname = xml_tools.open_config()
        try:
            g_xmltree = ET.parse(self.m_fname)
        except SyntaxError:
            xml_tools.create_empty_config_file(self.m_fname)
            g_xmltree = ET.parse(self.m_fname)
        self.m_root = g_xmltree.getroot()
        #self.read_house()
        self.read_lights()
        self.read_schedule()

    def read_house(self):
        l_count = 0
        l_sect = self.m_root.find('Houses')
        l_list = l_sect.iterfind('House')
        for l_house in l_list:
            #print 'Iterlist', l_house, l_list
            l_count += 1
            l_obj = house.HouseData()
            l_obj.Name = l_house.get('Name')
            l_obj.Key = int(l_house.get('Key'))
            l_obj.Street = l_house.findtext('Street')
            l_obj.City = l_house.findtext('City')
            l_obj.State = l_house.findtext('State')
            l_obj.ZipCode = l_house.findtext('ZipCode')
            l_obj.Active = l_house.findtext('Active')
            l_obj.Phone   = l_house.findtext('Phone')
            l_obj.Latitude = l_house.findtext('Latitude')
            l_obj.Longitude = l_house.findtext('Longitude')
            l_obj.TimeZone = l_house.findtext('TimeZone')
            l_obj.SavingTime = l_house.get('SavingTime')
            #print '  found name', l_obj.Name, l_obj.Street
            House_Data[l_obj.Key] = l_obj
        return l_count
            

    def read_lights(self):
        pass

    def read_schedule(self):
        l_sect = self.m_root.find('Schedules')
        l_list = l_sect.iterfind('House')
        for l_sched in l_list:
            pass


class WriteConfig(object):
    """Use the internal data to write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    m_filename = None
    m_root = None

    def __init__(self):
        print "WriteConfig XML"
        global g_xmltree
        self.m_filename = xml_tools.open_config()
        g_xmltree = ET.parse(self.m_filename)
        self.m_root = g_xmltree.getroot()
        #l_nice = xml_tools.prettify(self.m_root)
        #print l_nice

    def write_file(self):
        #l_fh = open(self.m_filename, 'w')
        #l_fh.write(xml_tools.prettify(self.m_root))
        g_xmltree.write(self.m_filename)

    def put_bool(self, p_arg):
        l_text = 'False'
        if p_arg != 0: l_text = 'True'
        return l_text

    def get_bool(self, p_arg):
        l_ret = 0
        if p_arg == 'True': l_ret = 1
        return l_ret

    def build_common(self, p_parent, p_title, p_obj):
        l_ret = ET.SubElement(p_parent, p_title)
        l_ret.set('Name', p_obj.Name)
        l_ret.set('Key', str(p_obj.Key))
        #print "build common - Name{0:} Active {1:}".format(p_obj.Name, p_obj.Active)
        ET.SubElement(l_ret, 'Active').text = self.put_bool(p_obj.Active)
        return l_ret

    def write_houses(self):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_sect = self.m_root.find('Houses')
        try:
            l_sect.clear()
        except AttributeError:
            l_sect = ET.SubElement(self.m_root, 'Houses')
        for l_obj in House_Data.itervalues():
            print "XLM writing houses: {0:}".format(l_obj.Name)
            l_house = self.build_common(l_sect, 'House', l_obj)
            ET.SubElement(l_house, 'Street').text = l_obj.Street
            ET.SubElement(l_house, 'City').text = l_obj.City
            ET.SubElement(l_house, 'State').text = l_obj.State
            ET.SubElement(l_house, 'ZipCode').text = l_obj.ZipCode
            ET.SubElement(l_house, 'Phone').text = l_obj.Phone
            ET.SubElement(l_house, 'Latitude').text = str(l_obj.Latitude)
            ET.SubElement(l_house, 'Longitude').text = str(l_obj.Longitude)
            ET.SubElement(l_house, 'TimeZone').text = str(l_obj.TimeZone)
            ET.SubElement(l_house, 'SavingTime').text = str(l_obj.SavingTime)
        self.write_file()

    def write_lights(self):
        l_sect = self.m_root.find('Lighting')
        try:
            l_sect.clear()
        except AttributeError:
            l_sect = ET.SubElement(self.m_root, 'Lighting')
        l_lgts = ET.SubElement(l_sect, 'Lights')
        l_ctls = ET.SubElement(l_sect, 'Controllers')
        l_btns = ET.SubElement(l_sect, 'Buttons')
        for l_obj in Light_Data.itervalues():
            l_lght = self.build_common(l_lgts, 'Light', l_obj)
            ET.SubElement(l_lght, 'Comment').text = l_obj.Comment
            ET.SubElement(l_lght, 'Dimmable').text = l_obj.Dimmable
            ET.SubElement(l_lght, 'Family').text = l_obj.Family
            ET.SubElement(l_lght, 'Room').text = l_obj.Room
            ET.SubElement(l_lght, 'Type').text = l_obj.Type
        for l_obj in Button_Data.itervalues():
            l_bttn = self.build_common(l_btns, 'Button', l_obj)
        for l_obj in Controller_Data.itervalues():
            l_ctlr = self.build_common(l_ctls, 'Controller', l_obj)
        self.write_file()

    def write_schedules(self):
        """Replace all the data in the 'Schedules' section with the current data.
        """
        l_sect = self.m_root.find('Schedules')
        try:
            l_sect.clear()
        except AttributeError:
            l_sect = ET.SubElement(self.m_root, 'Schedules')
        for l_obj in Schedule_Data.itervalues():
            #print "XLM writing schedule: {0:}".format(l_obj.Name)
            l_entry = self.build_common(l_sect, 'Schedule', l_obj)
            ET.SubElement(l_entry, 'Level').text = str(l_obj.Level)
            ET.SubElement(l_entry, 'LightName').text = l_obj.LightName
            ET.SubElement(l_entry, 'Rate').text = str(l_obj.Rate)
            ET.SubElement(l_entry, 'Time').text = l_obj.Time
            ET.SubElement(l_entry, 'Type').text = l_obj.Type
        self.write_file()

### END
