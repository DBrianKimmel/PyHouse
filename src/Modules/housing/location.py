"""
-*- test-case-name: PyHouse.src.Modules.housing.test.test_location -*-

@name: PyHouse/src/Modules/housing/location.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Handle the location information for a house.

There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations may be added such as
moon rise, tides, etc.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.utils import xml_tools
from Modules.Core.data_objects import LocationData

g_debug = 0
m_logger = None

class ReadWriteConfig(xml_tools.ConfigTools):
    """Use the internal data to read / write an updated XML config file.
    """

    def read_location_xml(self, p_house_xml):
        """
        @param p_house_obj: is p_pyhouses_obj.House.OBJs
        @param p_house_xml: is one of 0+ 'House' elements
        """
        l_location_obj = LocationData()
        l_location_xml = p_house_xml.find('Location')
        l_location_obj.Street = self.get_text_from_xml(l_location_xml, 'Street')
        l_location_obj.City = self.get_text_from_xml(l_location_xml, 'City')
        l_location_obj.State = self.get_text_from_xml(l_location_xml, 'State')
        l_location_obj.ZipCode = self.get_text_from_xml(l_location_xml, 'ZipCode')
        l_location_obj.Phone = self.get_text_from_xml(l_location_xml, 'Phone')
        l_location_obj.Latitude = self.get_float_from_xml(l_location_xml, 'Latitude')
        l_location_obj.Longitude = self.get_float_from_xml(l_location_xml, 'Longitude')
        l_location_obj.TimeZone = self.get_float_from_xml(l_location_xml, 'TimeZone')
        l_location_obj.SavingTime = self.get_float_from_xml(l_location_xml, 'SavingTime')
        return l_location_obj

    def write_location_xml(self, p_location_obj):
        """Replace the data in the 'House/Location' section with the current data.
        """
        l_entry = ET.Element('Location')
        self.put_text_element(l_entry, 'Street', p_location_obj.Street)
        self.put_text_element(l_entry, 'City', p_location_obj.City)
        self.put_text_element(l_entry, 'State', p_location_obj.State)
        self.put_text_element(l_entry, 'ZipCode', p_location_obj.ZipCode)
        self.put_text_element(l_entry, 'Phone', p_location_obj.Phone)
        self.put_float_element(l_entry, 'Latitude', p_location_obj.Latitude)
        self.put_float_element(l_entry, 'Longitude', p_location_obj.Longitude)
        self.put_float_element(l_entry, 'TimeZone', p_location_obj.TimeZone)
        self.put_float_element(l_entry, 'SavingTime', p_location_obj.SavingTime)
        return l_entry

# ## END DBK
