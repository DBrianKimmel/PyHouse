#!/usr/bin/env python

"""
"""

import sys
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

class ConfigTools(object):

    def get_bool(self, p_arg):
        l_ret = False
        if p_arg == 'True': l_ret = True
        return l_ret

    def get_float(self, p_obj, p_name):
        l_var = p_obj.findtext(p_name)
        try:
            l_var = float(l_var)
        except ValueError:
            l_var = 0.0
        return l_var
            
    def get_int(self, p_obj, p_name):
        l_var = p_obj.findtext(p_name)
        try:
            l_var = int(l_var)
        except ValueError:
            l_var = 0
        return l_var
            
    def put_bool(self, p_arg):
        l_text = 'False'
        if p_arg != False: l_text = 'True'
        return l_text

    def put_str(self, p_obj):
        try:
            l_var = str(p_obj)
        except AttributeError:
            l_var = 'no str value'
        return l_var

    def build_common(self, p_parent, p_title, p_obj):
        l_ret = ET.SubElement(p_parent, p_title)
        l_ret.set('Name', p_obj.Name)
        l_ret.set('Key', str(p_obj.Key))
        #print "build common - Name{0:} Active {1:}".format(p_obj.Name, p_obj.Active)
        ET.SubElement(l_ret, 'Active').text = self.put_bool(p_obj.Active)
        return l_ret


class ReadConfig(ConfigTools):
    """
    """

    def __init__(self):
        print "ReadConfig XML"
        global g_xmltree
        self.m_fname = xml_tools.open_config()
        try:
            g_xmltree = ET.parse(self.m_fname)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(self.m_fname)
            g_xmltree = ET.parse(self.m_fname)
        self.m_root = g_xmltree.getroot()


    def read_houses(self):
        l_count = 0
        try:
            l_sect = self.m_root.find('Houses')
            l_list = l_sect.iterfind('House')
        except AttributeError:
            print " -- Error in read_house - Adding 'Houses'"
            l_sect = ET.SubElement(self.m_root, 'Houses')
            l_list = l_sect.iterfind('House')
        for l_house in l_list:
            #print 'Iterlist', l_house, l_list
            l_count += 1
            l_obj = house.HouseData()
            l_obj.Active = self.get_bool(l_house.findtext('Active'))
            l_obj.Name = l_house.get('Name')
            l_obj.Key = int(l_house.get('Key'))
            l_obj.Street = l_house.findtext('Street')
            l_obj.City = l_house.findtext('City')
            l_obj.State = l_house.findtext('State')
            l_obj.ZipCode = l_house.findtext('ZipCode')
            l_obj.Phone   = l_house.findtext('Phone')
            l_obj.Latitude = self.get_float(l_house, 'Latitude')
            l_obj.Longitude = self.get_float(l_house, 'Longitude')
            l_obj.TimeZone = self.get_float(l_house, 'TimeZone')
            l_obj.SavingTime = self.get_float(l_house, 'SavingTime')
            #print '  found name', l_obj.Name, l_obj.Street
            House_Data[l_obj.Key] = l_obj
        return l_count

    def read_light_common(self, p_entry, p_obj):
        print "Read_light_common - Entry={0:}, Name={1:}".format(p_entry, p_entry.get('Name'))
        p_obj.Key = int(p_entry.get('Key'))
        p_obj.Name = p_entry.get('Name')
        p_obj.Active = self.get_bool(p_entry.get('Active'))
        p_obj.Comment = p_entry.findtext('Comment')
        p_obj.Coords = p_entry.findtext('Coords')
        p_obj.Dimmable = self.get_bool(p_entry.findtext('Dimmable'))
        p_obj.Family = l_fam = p_entry.findtext('Family')
        p_obj.Room = p_entry.findtext('Room')
        p_obj.Type = p_entry.findtext('Type')
        if l_fam == 'UPB':
            p_obj.NetworkID = l_fam = p_entry.findtext('NetworkID')
            p_obj.Password = p_entry.findtext('Password')
            p_obj.UnitID = p_entry.findtext('UnitID')
        elif l_fam == 'Insteon':
            p_obj.Address = p_entry.findtext('Address')
            p_obj.Controller = p_entry.findtext('Controller')
            p_obj.DevCat = p_entry.findtext('DevCat')
            p_obj.GroupList = p_entry.findtext('GroupList')
            p_obj.GroupNumber = p_entry.findtext('GroupNumber')
            p_obj.Master = p_entry.findtext('Master')
            p_obj.ProductKey = p_entry.findtext('ProductKey')
            p_obj.Responder = p_entry.findtext('Responder')
        return p_obj

    def read_lights(self):
        l_count = 0
        try:
            l_sect = self.m_root.find('Lighting')
            l_list = l_sect.iterfind('Controller') # use l_sect to force error if Lighting is missing
        except AttributeError:
            print " -- Error in read_lights - Adding 'Lighting'"
            l_sect = ET.SubElement(self.m_root, 'Lighting')
            l_l = ET.SubElement(l_sect, 'Lights')
            l_c = ET.SubElement(l_sect, 'Controllers')
            l_b = ET.SubElement(l_sect, 'Buttons')

        # read the lights section
        try:
            l_list = l_sect.iterfind('Lights')
            l_list = ET.SubElement(l_sect, 'Lights')
        except AttributeError:
            l_list = ET.SubElement(l_sect, 'Lights')
        for l_entry in l_list:
            l_obj = lighting.LightingData()
            print 'Lights Iterlist =', l_entry
            self.read_light_common(l_entry, l_obj)
            Light_Data[l_obj.Key] = l_obj
            l_count += 1

        # Read the controllers section
        try:
            l_list = l_sect.iterfind('Controller')
        except AttributeError:
            l_list = ET.SubElement(l_sect, 'Controllers')
        for l_entry in l_list:
            print 'Controller Iterlist', l_entry, l_list
            l_obj = lighting.ControllerData()
            self.read_light_common(l_entry, l_obj)
            l_obj.Interface = l_if = l_entry.findtext('Interface')
            l_obj.Port = l_entry.findtext('Port')
            if l_if == 'Serial':
                l_obj.BaudRate = l_entry.findtext('BaudRate')
                l_obj.ByteSize = l_entry.findtext('ByteSize')
                l_obj.DtsDtr = l_entry.findtext('DtsDtr')
                l_obj.InterCharTimeout = l_entry.findtext('InterCharTimeout')
                l_obj.Parity = l_entry.findtext('Parity')
                l_obj.RtsCts = l_entry.findtext('RtsCts')
                l_obj.StopBits = l_entry.findtext('StopBits')
                l_obj.Timeout = l_entry.findtext('Timeout')
                l_obj.WriteTimeout = l_entry.findtext('WriteTimeout')
                l_obj.XonXoff = l_entry.findtext('XonXoff')
            elif l_if == 'USB':
                l_obj.Product = l_entry.findtext('Product')
                l_obj.Vendor = l_entry.findtext('Vendor')
            Controller_Data[l_obj.Key] = l_obj
            l_count += 1

        # Read the button section
        try:
            l_list = l_sect.iterfind('Button')
        except AttributeError:
            l_list = ET.SubElement(l_sect, 'Buttons')
        for l_entry in l_list:
            l_obj = lighting.ButtonData()
            self.read_light_common(l_entry, l_obj)
            l_obj.Interface = l_entry.findtext('Interface')
            Controller_Data[l_obj.Key] = l_obj
            l_count += 1
        return l_count

    def read_schedules(self):
        l_count = 0
        try:
            l_sect = self.m_root.find('Schedules')
            l_list = l_sect.iterfind('Schedule')
        except AttributeError:
            print " -- Error in read_Schedules - Adding 'Schedules'"
            l_sect = ET.SubElement(self.m_root, 'Schedules')
            l_list = l_sect.iterfind('Schedule')
        for l_sched in l_list:
            pass


class WriteConfig(ConfigTools):
    """Use the internal data to write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    m_filename = None
    m_root = None

    def __init__(self):
        print "WriteConfig XML"
        global g_xmltree
        self.m_filename = xml_tools.open_config()
        try:
            g_xmltree = ET.parse(self.m_filename)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(self.m_filename)
            g_xmltree = ET.parse(self.m_filename)
        self.m_root = g_xmltree.getroot()


    def write_file(self):
        print "Writing config file named", self.m_filename
        g_xmltree.write(self.m_filename)

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

    def write_light_common(self, p_entry, p_obj):
        ET.SubElement(p_entry, 'Comment').text = str(p_obj.Comment)
        ET.SubElement(p_entry, 'Coords').text = str(p_obj.Coords)
        ET.SubElement(p_entry, 'Dimmable').text = self.put_bool(p_obj.Dimmable)
        ET.SubElement(p_entry, 'Family').text = p_obj.Family
        ET.SubElement(p_entry, 'Room').text = p_obj.Room
        ET.SubElement(p_entry, 'Type').text = p_obj.Type
        if p_obj.Family == 'Insteon':
            #print "WriteLightCommon Insteon=", p_obj
            ET.SubElement(p_entry, 'Address').text = p_obj.Address
            ET.SubElement(p_entry, 'Controller').text = str(p_obj.Controller)
            ET.SubElement(p_entry, 'DevCat').text = str(p_obj.DevCat)
            ET.SubElement(p_entry, 'GroupList').text = str(p_obj.GroupList)
            ET.SubElement(p_entry, 'GroupNumber').text = str(p_obj.GroupNumber)
            ET.SubElement(p_entry, 'Master').text = str(p_obj.Master)
            ET.SubElement(p_entry, 'ProductKey').text = str(p_obj.ProductKey)
            ET.SubElement(p_entry, 'Responder').text = str(p_obj.Responder)
        elif p_obj.Family == 'UPB':
            #print "WriteLightCommon UPB=", p_obj
            try:
                ET.SubElement(p_entry, 'NetworkID').text = self.put_str(p_obj.NetworkID)
                ET.SubElement(p_entry, 'Password').text = str(p_obj.Password)
                ET.SubElement(p_entry, 'UnitID').text = str(p_obj.UnitID)
            except AttributeError:
                pass
        
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
            l_entry = self.build_common(l_lgts, 'Light', l_obj)
            self.write_light_common(l_entry, l_obj)
        for l_obj in Button_Data.itervalues():
            l_entry = self.build_common(l_btns, 'Button', l_obj)
            self.write_light_common(l_entry, l_obj)
        for l_obj in Controller_Data.itervalues():
            l_entry = self.build_common(l_ctls, 'Controller', l_obj)
            self.write_light_common(l_entry, l_obj)
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

def read_config():
    l_rf = ReadConfig()
    l_rf.read_houses()
    l_rf.read_lights()
    l_rf.read_schedules()

def write_config():
    l_wf = WriteConfig()
    l_wf.write_houses()
    l_wf.write_lights()
    l_wf.write_schedules()
    
### END
