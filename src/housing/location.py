"""
Created on Apr 10, 2013

@author: briank

There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations may be added such as
moon rise, tides, etc.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools

g_debug = 0
m_logger = None

class LocationData(object):

    def __init__(self):
        self.City = ''
        self.Latitude = 0.0
        self.Longitude = 0.0
        self.Phone = ''
        self.SavingTime = 0.0
        self.State = ''
        self.Street = ''
        self.TimeZone = 0.0
        self.ZipCode = ''

    def __str__(self):
        l_ret = ' Location:: '
        l_ret += 'Addr:{0:} {1:} {2:} {3:}, '.format(self.Street, self.City, self.State, self.ZipCode)
        l_ret += 'Lat:{0:}, Lon:{1:}'.format(self.Latitude, self.Longitude)
        return l_ret


class ReadWriteConfig(xml_tools.ConfigTools):
    """Use the internal data to read / write an updated XML config file.
    """

    def read_location(self, p_house_obj, p_house_xml):
        l_location_obj = LocationData()
        if g_debug > 4:
            print "house.read_location() - Active=", p_house_obj.Active, p_house_obj.Name
        l_location_xml = p_house_xml.find('Location')
        l_location_obj.Street = self.get_text_element(l_location_xml, 'Street')
        l_location_obj.City = self.get_text_element(l_location_xml, 'City')
        l_location_obj.State = self.get_text_element(l_location_xml, 'State')
        l_location_obj.ZipCode = self.get_text_element(l_location_xml, 'ZipCode')
        l_location_obj.Phone = self.get_text_element(l_location_xml, 'Phone')
        l_location_obj.Latitude = self.get_float_element(l_location_xml, 'Latitude')
        l_location_obj.Longitude = self.get_float_element(l_location_xml, 'Longitude')
        l_location_obj.TimeZone = self.get_float_element(l_location_xml, 'TimeZone')
        l_location_obj.SavingTime = self.get_float_element(l_location_xml, 'SavingTime')
        p_house_obj.Location = l_location_obj
        if g_debug > 4:
            print "house.read_location()  loaded location for {0:}".format(p_house_obj.Name)
        return l_location_obj

    def write_location(self, p_location_obj):
        """Replace the data in the 'House/Location' section with the current data.
        """
        l_entry = ET.Element('Location')
        ET.SubElement(l_entry, 'Street').text = p_location_obj.Street
        ET.SubElement(l_entry, 'City').text = p_location_obj.City
        ET.SubElement(l_entry, 'State').text = p_location_obj.State
        ET.SubElement(l_entry, 'ZipCode').text = p_location_obj.ZipCode
        ET.SubElement(l_entry, 'Phone').text = p_location_obj.Phone
        ET.SubElement(l_entry, 'Latitude').text = str(p_location_obj.Latitude)
        ET.SubElement(l_entry, 'Longitude').text = str(p_location_obj.Longitude)
        ET.SubElement(l_entry, 'TimeZone').text = str(p_location_obj.TimeZone)
        ET.SubElement(l_entry, 'SavingTime').text = str(p_location_obj.SavingTime)
        if g_debug > 2:
            print "house.write_location()"
        return l_entry

# ## END DBK
